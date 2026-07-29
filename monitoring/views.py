from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from .streaming import generate_frames

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