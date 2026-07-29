import face_recognition
import numpy as np


def compute_encoding_from_image(image_path):
    """
    Load an image file, find the first face, and return its 128-d encoding
    as a NumPy array. Returns None if no face is found.
    """
    image = face_recognition.load_image_file(image_path)

    # Locate faces first (returns list of box coords)
    face_locations = face_recognition.face_locations(image)
    if not face_locations:
        return None

    # Compute encodings for found faces; take the first
    encodings = face_recognition.face_encodings(image, face_locations)
    if not encodings:
        return None

    return encodings[0]