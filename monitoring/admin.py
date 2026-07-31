from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("event_type", "level", "score", "created_at")
    list_filter = ("level", "event_type")