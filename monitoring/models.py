from django.db import models


class Event(models.Model):
    LEVEL_CHOICES = [
        ("LOW", "Low"), ("MEDIUM", "Medium"),
        ("HIGH", "High"), ("CRITICAL", "Critical"),
    ]
    event_type = models.CharField(max_length=50)      # e.g. "Unknown Visitor", "Loitering"
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default="LOW")
    score = models.IntegerField(default=0)
    detail = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.event_type} ({self.level}) @ {self.created_at:%H:%M:%S}"