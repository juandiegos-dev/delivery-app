from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from pedidos.models import Pedido
from repartidores.models import Asignacion, HistorialUbicacion, PerfilRepartidor, PuntoRestaurante

def pedido_visible(pedido_id, usuario):
    return get_object_or_404(Pedido.objects.filter(
        Q(cliente=usuario) | Q(restaurante__dueno=usuario) | 
        Q(asignacion__repartidor=usuario)
    ).distinct(), pk=pedido_id)

class RutaPedidoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pedido_id):
        pedido = pedido_visible(pedido_id, request.user)
        punto = PuntoRestaurante.objects.filter(restaurante=pedido.restaurante).first()
        asignacion = Asignacion.objects.filter(pedido=pedido).select_related("repartidor").first()
        perfil = (PerfilRepartidor.objects.filter(usuario=asignacion.repartidor).first()
                  if asignacion else None)
        trayecto = (list(HistorialUbicacion.objects.filter(asignacion=asignacion)
                         .order_by("registrado_en", "id")
                         .values("latitud", "longitud", "registrado_en"))
                   if asignacion else [])
        return Response({
            "pedido": pedido.pk,
            "estado": pedido.estado,
            "restaurante": ({"latitud": punto.latitud, "longitud": punto.longitud} if punto else None),
            "repartidor": ({"username": asignacion.repartidor.username,
                            "latitud": perfil.latitud, "longitud": perfil.longitud}
                           if asignacion and perfil else None),
            "actualizacion": perfil.actualizado_en if perfil else None,
            "trayecto": trayecto,
        })