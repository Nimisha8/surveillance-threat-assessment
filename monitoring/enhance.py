import cv2


class LowLightEnhancer:
    """
    Enhances contrast in dark frames using CLAHE on the L (lightness) channel
    of the LAB color space, so brightness improves without color distortion.

    clip_limit: caps contrast boost (higher = stronger, but more noise)
    tile_size:  size of local regions equalized independently
    """
    def __init__(self, clip_limit=3.0, tile_size=8):
        self.clahe = cv2.createCLAHE(
            clipLimit=clip_limit,
            tileGridSize=(tile_size, tile_size)
        )

    def enhance(self, frame):
        # Split brightness from color: LAB = Lightness, A, B
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        # Apply CLAHE to the lightness channel only
        l = self.clahe.apply(l)

        # Merge back and convert to BGR
        lab = cv2.merge((l, a, b))
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)