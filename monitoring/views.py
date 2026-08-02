from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from .streaming import generate_frames
from django.http import JsonResponse
from .models import Event
# For now, source=0 = your webcam. Later we'll swap to a demo video file
# by changing this one value (or making it configurable).
VIDEO_SOURCE = 0


@login_required
def video_feed(request):
    """Streams MJPEG. This is what the <img> tag points at."""
    return StreamingHttpResponse(
        generate_frames(VIDEO_SOURCE),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )



@login_required
def latest_threat(request):
    """Return the most recent event as JSON, for the browser to poll."""
    e = Event.objects.first()  # ordering is -created_at, so first = newest
    if e is None:
        return JsonResponse({"id": None})
    return JsonResponse({
        "id": e.id,
        "type": e.event_type,
        "level": e.level,
        "score": e.score,
        "detail": e.detail,
    })