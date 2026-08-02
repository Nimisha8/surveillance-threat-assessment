import cv2
import time


class VideoSource:
    """
    Wraps OpenCV video capture. Webcam index (0) or file path.
    DirectShow backend on Windows for stability; retries transient read failures.
    """
    def __init__(self, source=0):
        self.source = source
        self.cap = None
        if isinstance(source, int):
            self.cap = cv2.VideoCapture(source, cv2.CAP_DSHOW)
        else:
            self.cap = cv2.VideoCapture(source)

        # These must come AFTER self.cap exists
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def read(self):
        for _ in range(3):
            success, frame = self.cap.read()
            if success and frame is not None:
                return frame
            time.sleep(0.05)
        return None

    def release(self):
        if self.cap is not None:
            self.cap.release()

    def __del__(self):
        if getattr(self, "cap", None) is not None:
            self.cap.release()