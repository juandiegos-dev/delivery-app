from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from notificaciones.models import Notificacion
from notificaciones.serializers import NotificacionSerializer


class MisNotificacionesView(generics.ListAPIView):
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notificacion.objects.filter(destinatario=self.request.user)