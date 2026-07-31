import time
from .models import Event


class EventLogger:
    """Logs events to the DB, throttled so we don't spam one row per frame."""
    def __init__(self, cooldown=5):
        self.cooldown = cooldown          # seconds between same-type logs
        self._last = {}                   # event_type -> last logged time

    def log(self, event_type, level, score, detail=""):
        now = time.time()
        if now - self._last.get(event_type, 0) < self.cooldown:
            return
        self._last[event_type] = now
        Event.objects.create(
            event_type=event_type, level=level, score=score, detail=detail
        )