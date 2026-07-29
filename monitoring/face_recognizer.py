import cv2
import numpy as np
import face_recognition
from useraccounts.models import AuthorizedUser


class FaceRecognizer:
    """
    Recognizes faces against enrolled AuthorizedUsers.
    Loads stored 128-d encodings once, then compares live faces by distance.
    """
    def __init__(self, tolerance=0.5, scale=0.25):
        self.tolerance = tolerance      # lower = stricter match
        self.scale = scale              # downscale factor for detection speed
        self.known_encodings = []
        self.known_names = []
        self.load_known_faces()

    def load_known_faces(self):
        """Load all enrolled encodings from the database into memory."""
        self.known_encodings = []
        self.known_names = []
        for user in AuthorizedUser.objects.all():
            enc = user.get_encoding()
            if enc:
                self.known_encodings.append(np.array(enc))
                self.known_names.append(user.name)

    def recognize(self, frame):
        """Return (annotated_frame, names_found_list)."""
        # Downscale for faster detection
        small = cv2.resize(frame, (0, 0), fx=self.scale, fy=self.scale)
        # face_recognition uses RGB; OpenCV frames are BGR
        rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

        locations = face_recognition.face_locations(rgb_small)
        encodings = face_recognition.face_encodings(rgb_small, locations)

        names_found = []
        for (top, right, bottom, left), face_enc in zip(locations, encodings):
            name = "Unknown"
            color = (0, 0, 255)  # red for unknown

            if self.known_encodings:
                distances = face_recognition.face_distance(self.known_encodings, face_enc)
                best = np.argmin(distances)
                if distances[best] <= self.tolerance:
                    name = self.known_names[best]
                    color = (0, 200, 0)  # green for known

            names_found.append(name)

            # Scale coordinates back up to full-size frame
            factor = int(1 / self.scale)
            top, right, bottom, left = top*factor, right*factor, bottom*factor, left*factor

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        return frame, names_found