import cv2
from .video import VideoSource
from .motion import MotionDetector
from .enhance import LowLightEnhancer
from .detection import HumanDetector
from .face_recognizer import FaceRecognizer

ENABLE_LOW_LIGHT = True
ENABLE_MOTION = True
ENABLE_HUMAN = True
ENABLE_FACE = True

FACE_EVERY_N = 3   # run face recognition every Nth frame for speed


def generate_frames(source=0):
    video = VideoSource(source)
    detector = MotionDetector(threshold=25, min_area=500)
    enhancer = LowLightEnhancer(clip_limit=3.0, tile_size=8)
    human = HumanDetector(model_path="yolov8n.pt", conf_threshold=0.5)
    recognizer = FaceRecognizer(tolerance=0.6, scale=0.25)

    frame_count = 0
    last_face_boxes = []

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

            if ENABLE_HUMAN:
                frame, people = human.detect(frame)

            if ENABLE_FACE and frame_count % FACE_EVERY_N == 0:
                frame, names = recognizer.recognize(frame)

            success, buffer = cv2.imencode(".jpg", frame)
            if not success:
                continue

            jpeg_bytes = buffer.tobytes()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg_bytes + b"\r\n"
            )
    finally:
        video.release()