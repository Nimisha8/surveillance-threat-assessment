import cv2


class MotionDetector:
    """
    Detects motion by comparing each frame to the previous one (frame differencing).
    Stateful: it remembers the previous frame between calls.

    Tunable sensitivity:
      - threshold: pixel-change cutoff (lower = more sensitive)
      - min_area:  smallest moving blob (in pixels) that counts as motion
    """
    def __init__(self, threshold=25, min_area=500):
        self.threshold = threshold
        self.min_area = min_area
        self.prev_gray = None

    def _preprocess(self, frame):
        # Step 1: grayscale (motion cares about brightness change, not color)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Step 2: blur to suppress pixel-level sensor noise
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        return gray

    def process(self, frame):
        """
        Returns (annotated_frame, motion_detected_bool).
        Draws green boxes around regions where motion is found.
        """
        gray = self._preprocess(frame)

        # First frame ever: nothing to compare against yet
        if self.prev_gray is None:
            self.prev_gray = gray
            return frame, False

        # Step 3: absolute difference between previous and current
        delta = cv2.absdiff(self.prev_gray, gray)

        # Step 4: threshold -> pure black/white motion mask
        thresh = cv2.threshold(delta, self.threshold, 255, cv2.THRESH_BINARY)[1]

        # Step 5: dilate to fill gaps so a person reads as one solid blob
        thresh = cv2.dilate(thresh, None, iterations=2)

        # Step 6: find outlines of the white (motion) regions
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        motion_detected = False
        for c in contours:
            if cv2.contourArea(c) < self.min_area:
                continue  # too small, ignore as noise
            motion_detected = True
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Update memory for the next frame
        self.prev_gray = gray

        # Optional on-screen label
        if motion_detected:
            cv2.putText(frame, "MOTION DETECTED", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        return frame, motion_detected