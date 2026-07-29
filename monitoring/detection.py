from ultralytics import YOLO
import cv2


class HumanDetector:
    """
    Detects people in a frame using a YOLO model pretrained on COCO.
    COCO class 0 = 'person'. We keep only that class.

    conf_threshold: minimum confidence to accept a detection (0-1).
    """
    # COCO class id for 'person'
    PERSON_CLASS_ID = 0

    def __init__(self, model_path="yolov8n.pt", conf_threshold=0.5):
        # Loads (and on first run, downloads) the nano model
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold

    def detect(self, frame):
        """
        Returns (annotated_frame, person_count).
        Draws a box + confidence label around each detected person.
        """
        # verbose=False stops YOLO printing to the console every frame
        results = self.model(frame, verbose=False)

        person_count = 0

        # results is a list (one item per image); we passed one frame
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                # Keep only people above our confidence threshold
                if class_id != self.PERSON_CLASS_ID:
                    continue
                if confidence < self.conf_threshold:
                    continue

                person_count += 1

                # Box coordinates (x1,y1) top-left, (x2,y2) bottom-right
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 128, 0), 2)

                label = f"Person {confidence:.2f}"
                cv2.putText(frame, label, (x1, y1 - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 128, 0), 2)

        # Show the live head-count top-right-ish
        cv2.putText(frame, f"People: {person_count}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        return frame, person_count