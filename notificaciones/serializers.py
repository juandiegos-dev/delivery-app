from rest_framework import serializers
from notificaciones.models import Notificacion


class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ["id", "pedido", "tipo", "mensaje", "leida", "fecha"]
        read_only_fields = fields