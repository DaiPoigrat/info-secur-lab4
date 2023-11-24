from django.urls import path
from .views import registrate, auth, refresh
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('registrate', csrf_exempt(registrate)),
    path('auth', csrf_exempt(auth)),
    path('refresh', csrf_exempt(refresh)),
]
