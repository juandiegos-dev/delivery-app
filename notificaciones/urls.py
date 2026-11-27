from django.urls import path
from notificaciones.views import MisNotificacionesView

urlpatterns = [
    path("", MisNotificacionesView.as_view()),
]