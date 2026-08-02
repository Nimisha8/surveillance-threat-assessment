import time
import cv2
from django.core.files.base import ContentFile
from .models import Event


class EventLogger:
    """Logs events to the DB (throttled), optionally saving a snapshot frame."""
    def __init__(self, cooldown=5):
        self.cooldown = cooldown
        self._last = {}

    def log(self, event_type, level, score, detail="", frame=None):
        now = time.time()
        if now - self._last.get(event_type, 0) < self.cooldown:
            return None
        self._last[event_type] = now

        event = Event(event_type=event_type, level=level, score=score, detail=detail)

        # Attach a snapshot of the triggering frame, if provided
        if frame is not None:
            ok, buf = cv2.imencode(".jpg", frame)
            if ok:
                filename = f"{event_type.replace(' ', '_')}_{int(now)}.jpg"
                event.snapshot.save(filename, ContentFile(buf.tobytes()), save=False)

        event.save()
        return event