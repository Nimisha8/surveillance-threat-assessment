import cv2


class VideoSource:
    """
    Wraps OpenCV video capture. Accepts a webcam index (0) or a file path.
    All camera logic lives here so the rest of the system is source-agnostic.
    """
    def __init__(self, source=0):
        self.source = source
        self.cap = cv2.VideoCapture(source)

    def read(self):
        """Return one frame (a NumPy array) or None if the stream ended/failed."""
        success, frame = self.cap.read()
        if not success:
            return None
        return frame

    def release(self):
        self.cap.release()

    def __del__(self):
        # Ensure the camera is freed when the object is garbage-collected
        if self.cap is not None:
            self.cap.release()