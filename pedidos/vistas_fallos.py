"""RF12. Endpoint de fallo: restaurante o repartidor asignado."""
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from pedidos.fallos import registrar_fallo
from pedidos.models import Pedido
from pedidos.serializers import PedidoSerializer


class MotivoFalloSerializer(serializers.Serializer):
    motivo = serializers.CharField(min_length=8, max_length=300, trim_whitespace=True)


class FallarPedidoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        entrada = MotivoFalloSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        get_object_or_404(Pedido.objects.filter(
            Q(restaurante__dueno=request.user) | Q(asignacion__repartidor=request.user)
        ).distinct(), pk=pk)
        pedido = registrar_fallo(pk, request.user, entrada.validated_data["motivo"])
        return Response(PedidoSerializer(pedido).data)