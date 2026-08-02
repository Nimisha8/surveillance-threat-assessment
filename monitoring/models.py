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
    snapshot = models.ImageField(upload_to="snapshots/", blank=True, null=True)


    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.event_type} ({self.level}) @ {self.created_at:%H:%M:%S}"
class SystemSettings(models.Model):
    """Single-row table holding tunable detection/threat parameters."""
    motion_threshold = models.IntegerField(default=25)
    loiter_seconds = models.IntegerField(default=8)
    unknown_seconds = models.IntegerField(default=3)
    unattended_seconds = models.IntegerField(default=5)
    weight_unknown = models.IntegerField(default=40)
    weight_loitering = models.IntegerField(default=25)
    weight_unattended = models.IntegerField(default=30)
    

    def __str__(self):
        return "System Settings"

    @classmethod
    def load(cls):
        """Always return the single settings row, creating it if needed."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj