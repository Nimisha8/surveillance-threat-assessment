import cv2
from .video import VideoSource
from .motion import MotionDetector
from .enhance import LowLightEnhancer
from .detection import HumanDetector
from .face_recognizer import FaceRecognizer
from .tracker import CentroidTracker
from .threat import ThreatEngine
from .event_logger import EventLogger

ENABLE_LOW_LIGHT = False
ENABLE_MOTION = True
ENABLE_HUMAN = True
ENABLE_FACE = True

FACE_EVERY_N = 3
LOITER_SECONDS = 8
ASSUMED_FPS = 10
UNKNOWN_MIN_SECONDS = 3
UNATTENDED_SECONDS = 5          # object alone this long -> unattended
PERSON_NEAR_DISTANCE = 150      # px; person within this = "attended"


def point_in_box(point, box):
    px, py = point
    x1, y1, x2, y2 = box[:4]
    return x1 <= px <= x2 and y1 <= py <= y2


def box_center(box):
    x1, y1, x2, y2 = box[:4]
    return ((x1 + x2) // 2, (y1 + y2) // 2)


def distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def generate_frames(source=0):
    video = VideoSource(source)
    detector = MotionDetector(threshold=25, min_area=500)
    enhancer = LowLightEnhancer(clip_limit=3.0, tile_size=8)
    human = HumanDetector(model_path="yolov8n.pt", conf_threshold=0.5)
    recognizer = FaceRecognizer(tolerance=0.6, scale=0.25)
    tracker = CentroidTracker(max_disappeared=40, max_distance=80)
    object_tracker = CentroidTracker(max_disappeared=30, max_distance=60)
    threat_engine = ThreatEngine()
    logger = EventLogger(cooldown=5)

    id_authorized = {}
    frame_count = 0
    last_faces = []

    try:
        while True:
            frame = video.read()
            if frame is None:
                break

            frame_count += 1

            if ENABLE_LOW_LIGHT:
                frame = enhancer.enhance(frame)
            if ENABLE_MOTION:
                frame, motion = detector.process(frame)

            person_boxes = []
            object_boxes = []
            if ENABLE_HUMAN:
                frame, people, person_boxes, object_boxes = human.detect(frame)

            if ENABLE_FACE and frame_count % FACE_EVERY_N == 0:
                frame, last_faces = recognizer.recognize(frame)

            tracked = tracker.update(person_boxes)

            # associate faces -> person IDs
            id_to_box = {}
            for object_id, (centroid, frames_seen) in tracked.items():
                for b in person_boxes:
                    if point_in_box(centroid, b):
                        id_to_box[object_id] = b
                        break
            for name, face_center in last_faces:
                for object_id, box in id_to_box.items():
                    if point_in_box(face_center, box):
                        if name != "Unknown":
                            id_authorized[object_id] = True
                        else:
                            id_authorized.setdefault(object_id, False)
                        break

            loitering_ids, unknown_ids = [], []
            for object_id, (centroid, frames_seen) in tracked.items():
                cx, cy = centroid
                seconds_present = frames_seen / ASSUMED_FPS
                is_loitering = seconds_present >= LOITER_SECONDS
                is_authorized = id_authorized.get(object_id, False)
                is_unknown_visitor = (not is_authorized) and seconds_present >= UNKNOWN_MIN_SECONDS

                if is_unknown_visitor:
                    color = (0, 0, 255); label = f"ID {object_id} UNKNOWN"; unknown_ids.append(object_id)
                elif is_authorized:
                    color = (0, 200, 0); label = f"ID {object_id} AUTH"
                else:
                    color = (0, 255, 255); label = f"ID {object_id}"

                if is_loitering:
                    label += f" LOITER {int(seconds_present)}s"; loitering_ids.append(object_id)

                cv2.putText(frame, label, (cx - 10, cy - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                cv2.circle(frame, (cx, cy), 4, color, -1)

            # --- Unattended object logic ---
            obj_tracked = object_tracker.update(object_boxes)
            person_centers = [box_center(b) for b in person_boxes]
            unattended_ids = []
            for obj_id, (centroid, frames_seen) in obj_tracked.items():
                seconds_present = frames_seen / ASSUMED_FPS
                # nearest person distance
                nearest = min((distance(centroid, pc) for pc in person_centers), default=99999)
                attended = nearest <= PERSON_NEAR_DISTANCE
                is_unattended = (not attended) and seconds_present >= UNATTENDED_SECONDS

                cx, cy = centroid
                if is_unattended:
                    unattended_ids.append(obj_id)
                    cv2.putText(frame, "UNATTENDED", (cx - 20, cy),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            # --- Threat scoring ---
            per_person_unknown = len(unknown_ids)
            frame_score = threat_engine.score(
                is_unknown=len(unknown_ids) > 0,
                is_loitering=len(loitering_ids) > 0,
                unattended_count=len(unattended_ids),
                unknown_count=per_person_unknown,
            )
            level, level_color = threat_engine.classify(frame_score)

            # Log meaningful events (throttled)
            if loitering_ids:
                logger.log("Loitering", level, frame_score, f"{len(loitering_ids)} person(s)")
            if unknown_ids:
                logger.log("Unknown Visitor", level, frame_score, f"{len(unknown_ids)} unknown")
            if unattended_ids:
                logger.log("Unattended Object", level, frame_score, f"{len(unattended_ids)} object(s)")

            # Banners
            y = 90
            for text, active in [("LOITERING DETECTED", loitering_ids),
                                 ("UNKNOWN VISITOR", unknown_ids),
                                 ("UNATTENDED OBJECT", unattended_ids)]:
                if active:
                    cv2.putText(frame, text, (10, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    y += 28

            # Threat score box (top-right)
            h, w = frame.shape[:2]
            cv2.rectangle(frame, (w - 260, 10), (w - 10, 70), (0, 0, 0), -1)
            cv2.putText(frame, f"THREAT: {level}", (w - 250, 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, level_color, 2)
            cv2.putText(frame, f"Score: {frame_score}", (w - 250, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, level_color, 2)

            success, buffer = cv2.imencode(".jpg", frame)
            if not success:
                continue
            jpeg_bytes = buffer.tobytes()
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + jpeg_bytes + b"\r\n")
    finally:
        video.release()