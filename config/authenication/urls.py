from django.urls import path
from .views import registrate
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('registrate', csrf_exempt(registrate)),
    # path('auth', ),
]
