from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('live/', views.live_monitoring, name='live'),
    path('alerts/', views.alerts, name='alerts'),
    path('threats/', views.threats, name='threats'),
    path('history/', views.history, name='history'),
    path('authorized/', views.authorized_users, name='authorized'),
    path('unknown/', views.unknown_visitors, name='unknown'),
    path('analytics/', views.analytics, name='analytics'),
    path('settings/', views.settings_page, name='settings'),
    path('logs/', views.system_logs, name='logs'),
]