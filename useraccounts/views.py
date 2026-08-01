from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from monitoring.models import Event
from useraccounts.models import AuthorizedUser


@login_required
def dashboard(request):
    ctx = {
        "total_events": Event.objects.count(),
        "unknown_count": Event.objects.filter(event_type="Unknown Visitor").count(),
        "recent": Event.objects.all()[:5],
        "authorized_count": AuthorizedUser.objects.count(),
    }
    return render(request, "dashboard.html", ctx)


@login_required
def live_monitoring(request):
    return render(request, "live.html")


@login_required
def alerts(request):
    return render(request, "alerts.html", {"events": Event.objects.all()[:50]})


@login_required
def threats(request):
    events = Event.objects.filter(level__in=["HIGH", "CRITICAL"])[:50]
    return render(request, "threats.html", {"events": events})


@login_required
def history(request):
    return render(request, "history.html", {"events": Event.objects.all()[:100]})


@login_required
def authorized_users(request):
    return render(request, "authorized.html", {"users": AuthorizedUser.objects.all()})


@login_required
def unknown_visitors(request):
    events = Event.objects.filter(event_type="Unknown Visitor")[:50]
    return render(request, "unknown.html", {"events": events})


@login_required
def analytics(request):
    return render(request, "analytics.html", {
        "total": Event.objects.count(),
        "loitering": Event.objects.filter(event_type="Loitering").count(),
        "unknown": Event.objects.filter(event_type="Unknown Visitor").count(),
        "unattended": Event.objects.filter(event_type="Unattended Object").count(),
    })


@login_required
def settings_page(request):
    from monitoring.models import SystemSettings
    s = SystemSettings.load()
    if request.method == "POST":
        s.motion_threshold = int(request.POST.get("motion_threshold", s.motion_threshold))
        s.loiter_seconds = int(request.POST.get("loiter_seconds", s.loiter_seconds))
        s.unknown_seconds = int(request.POST.get("unknown_seconds", s.unknown_seconds))
        s.unattended_seconds = int(request.POST.get("unattended_seconds", s.unattended_seconds))
        s.weight_unknown = int(request.POST.get("weight_unknown", s.weight_unknown))
        s.weight_loitering = int(request.POST.get("weight_loitering", s.weight_loitering))
        s.weight_unattended = int(request.POST.get("weight_unattended", s.weight_unattended))
        s.save()
        saved = True
    else:
        saved = False
    return render(request, "settings.html", {"s": s, "saved": saved})


@login_required
def system_logs(request):
    return render(request, "logs.html", {"events": Event.objects.all()[:100]})