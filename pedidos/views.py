from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accesos.permissions import rol_requerido
from pedidos import services
from pedidos.models import Pedido
from pedidos.serializers import CambioEstadoSerializer, PedidoCrearSerializer, PedidoSerializer


class PedidoCrearView(APIView):
    permission_classes = [rol_requerido("cliente")]

    def post(self, request):
        entrada = PedidoCrearSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        pedido = services.crear_pedido(request.user, entrada.validated_data)
        return Response(PedidoSerializer(pedido).data, status=201)


class MisPedidosView(generics.ListAPIView):
    serializer_class = PedidoSerializer
    permission_classes = [rol_requerido("cliente")]

    def get_queryset(self):
        return Pedido.objects.filter(cliente=self.request.user).order_by("-id")


class PedidosRecibidosView(generics.ListAPIView):
    serializer_class = PedidoSerializer
    permission_classes = [rol_requerido("restaurante")]

    def get_queryset(self):
        return Pedido.objects.filter(restaurante__dueno=self.request.user).order_by("-id")


class PedidoDetalleView(generics.RetrieveAPIView):
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  # un usuario ajeno recibe 404, sin enterarse de que el pedido existe
        usuario = self.request.user
        return Pedido.objects.filter(Q(cliente=usuario) | Q(restaurante__dueno=usuario))

class CambiarEstadoView(APIView):
    permission_classes = [rol_requerido("restaurante")]

    def patch(self, request, pk):
        pedido = get_object_or_404(
            Pedido,
            pk=pk,
            restaurante__dueno=request.user
        )
        entrada = CambioEstadoSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)

        pedido = services.cambiar_estado(
            pedido,
            entrada.validated_data["estado"]
        )

        return Response(PedidoSerializer(pedido).data, status=200)

class CotizarEnvioView(APIView):

    permission_classes = [rol_requerido("cliente")]

    def get(self, request, restaurante_id):

        from catalogo.models import Restaurante
        from pedidos.tarifas import calcular_tarifa_envio

        restaurante = get_object_or_404(
            Restaurante,
            pk=restaurante_id
        )

        costo = calcular_tarifa_envio(restaurante)

        return Response({
            "restaurante": restaurante.id,
            "costo_envio": str(costo)
        })