from ultralytics import YOLO
import cv2


class HumanDetector:
    PERSON_CLASS_ID = 0
    # COCO ids for bag-like objects
    OBJECT_CLASS_IDS = {24: "backpack", 26: "handbag", 28: "suitcase"}

    def __init__(self, model_path="yolov8n.pt", conf_threshold=0.5):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold

    def detect(self, frame):
        """
        Returns (annotated_frame, person_count, person_boxes, object_boxes).
        object_boxes: list of (x1, y1, x2, y2, label).
        """
        results = self.model(frame, verbose=False)
        person_count = 0
        person_boxes = []
        object_boxes = []

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                if confidence < self.conf_threshold:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                if class_id == self.PERSON_CLASS_ID:
                    person_count += 1
                    person_boxes.append((x1, y1, x2, y2))
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 128, 0), 2)
                    cv2.putText(frame, f"Person {confidence:.2f}", (x1, y1 - 8),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 128, 0), 2)

                elif class_id in self.OBJECT_CLASS_IDS:
                    label = self.OBJECT_CLASS_IDS[class_id]
                    object_boxes.append((x1, y1, x2, y2, label))
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (200, 0, 200), 2)
                    cv2.putText(frame, label, (x1, y1 - 8),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 0, 200), 2)

        cv2.putText(frame, f"People: {person_count}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        return frame, person_count, person_boxes, object_boxes