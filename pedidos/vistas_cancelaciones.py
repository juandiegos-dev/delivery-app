"""RF11. Endpoint de cancelación: solo cliente propietario o dueño."""

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pedidos.cancelaciones import cancelar
from pedidos.models import Pedido
from pedidos.serializers import PedidoSerializer


class MotivoCancelacionSerializer(serializers.Serializer):
    motivo = serializers.CharField(
        min_length=8,
        max_length=300,
        trim_whitespace=True
    )


class CancelarPedidoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        entrada = MotivoCancelacionSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)

        # Ocultar pedidos ajenos mediante respuesta 404.
        get_object_or_404(
            Pedido.objects.filter(
                Q(cliente=request.user) |
                Q(restaurante__dueno=request.user)
            ),
            pk=pk
        )

        pedido = cancelar(
            pk,
            request.user,
            entrada.validated_data["motivo"]
        )

        return Response(PedidoSerializer(pedido).data)