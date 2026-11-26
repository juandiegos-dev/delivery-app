from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from pedidos.models import Pedido
from pedidos.serializers import PedidoSerializer
from repartidores.entregas import iniciar_reparto, confirmar_entrega


class IniciarRepartoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pedido_id):
        if request.user.rol != "repartidor":
            raise PermissionDenied("Solo un repartidor puede iniciar la entrega")
        get_object_or_404(Pedido.objects.filter(
            Q(asignacion__repartidor=request.user)
        ), pk=pedido_id)
        pedido = iniciar_reparto(pedido_id, request.user)
        return Response(PedidoSerializer(pedido).data)


class ConfirmarEntregaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pedido_id):
        if request.user.rol != "repartidor":
            raise PermissionDenied("Solo un repartidor puede confirmar la entrega")
        get_object_or_404(Pedido.objects.filter(
            Q(asignacion__repartidor=request.user)
        ), pk=pedido_id)
        pedido = confirmar_entrega(pedido_id, request.user)
        return Response(PedidoSerializer(pedido).data)

class MisAsignacionesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.rol != "repartidor":
            raise PermissionDenied("Solo los repartidores consultan sus asignaciones")
        from repartidores.models import Asignacion
        lista = Asignacion.objects.filter(
            repartidor=request.user,
            pedido__estado__in=[Pedido.Estado.LISTO, Pedido.Estado.EN_CAMINO],
        ).select_related("pedido").order_by("-id")
        return Response([{
            "pedido": a.pedido_id,
            "estado": a.pedido.estado,
            "direccion_entrega": a.pedido.direccion_entrega,
            "distancia_km": str(a.distancia_km),
        } for a in lista])