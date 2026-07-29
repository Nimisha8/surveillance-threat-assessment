from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def live_monitoring(request):
    return render(request, 'live.html')

@login_required
def alerts(request):
    return render(request, 'alerts.html')

@login_required
def threats(request):
    return render(request, 'threats.html')

@login_required
def history(request):
    return render(request, 'history.html')

@login_required
def authorized_users(request):
    return render(request, 'authorized.html')

@login_required
def unknown_visitors(request):
    return render(request, 'unknown.html')

@login_required
def analytics(request):
    return render(request, 'analytics.html')

@login_required
def settings_page(request):
    return render(request, 'settings.html')

@login_required
def system_logs(request):
    return render(request, 'logs.html')