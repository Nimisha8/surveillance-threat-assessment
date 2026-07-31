import cv2
import numpy as np
import face_recognition
from useraccounts.models import AuthorizedUser


class FaceRecognizer:
    def __init__(self, tolerance=0.6, scale=0.25):
        self.tolerance = tolerance
        self.scale = scale
        self.known_encodings = []
        self.known_names = []
        self.load_known_faces()

    def load_known_faces(self):
        self.known_encodings = []
        self.known_names = []
        for user in AuthorizedUser.objects.all():
            enc = user.get_encoding()
            if enc:
                self.known_encodings.append(np.array(enc))
                self.known_names.append(user.name)

    def recognize(self, frame):
        """
        Returns (annotated_frame, faces) where faces is a list of
        (name, (center_x, center_y)) for each detected face.
        """
        small = cv2.resize(frame, (0, 0), fx=self.scale, fy=self.scale)
        rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

        locations = face_recognition.face_locations(rgb_small)
        encodings = face_recognition.face_encodings(rgb_small, locations)

        faces = []
        factor = int(1 / self.scale)

        for (top, right, bottom, left), face_enc in zip(locations, encodings):
            name = "Unknown"
            color = (0, 0, 255)

            if self.known_encodings:
                distances = face_recognition.face_distance(self.known_encodings, face_enc)
                best = np.argmin(distances)
                if distances[best] <= self.tolerance:
                    name = self.known_names[best]
                    color = (0, 200, 0)

            # Scale back to full frame
            top, right, bottom, left = top*factor, right*factor, bottom*factor, left*factor
            center = ((left + right) // 2, (top + bottom) // 2)
            faces.append((name, center))

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        return frame, faces