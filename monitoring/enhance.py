import cv2
import numpy as np


class LowLightEnhancer:
    """
    Enhances contrast in dark frames using CLAHE on the L (lightness) channel
    of LAB color space. Only applies when the scene is actually dark, so
    well-lit frames render normally (no washed-out over-processing).

    brightness_threshold: mean brightness (0-255) below which we enhance.
    """
    def __init__(self, clip_limit=2.0, tile_size=8, brightness_threshold=90):
        self.clahe = cv2.createCLAHE(
            clipLimit=clip_limit,
            tileGridSize=(tile_size, tile_size)
        )
        self.brightness_threshold = brightness_threshold

    def _mean_brightness(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return float(np.mean(gray))

    def enhance(self, frame):
        # Skip enhancement entirely if the scene is already bright enough
        if self._mean_brightness(frame) >= self.brightness_threshold:
            return frame

        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        l = self.clahe.apply(l)
        lab = cv2.merge((l, a, b))
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)