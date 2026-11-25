from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from accesos.permissions import rol_requerido
from catalogo.models import Restaurante
from pedidos.models import Pedido
from repartidores.models import Asignacion, HistorialUbicacion, PerfilRepartidor, PuntoRestaurante
from repartidores.serializers import (AsignacionSerializer, CoordenadasSerializer,
    MiUbicacionSerializer, PerfilRepartidorSerializer, PuntoRestauranteSerializer)


class MiUbicacionView(APIView):
    permission_classes = [rol_requerido("repartidor")]

    def get(self, request):
        perfil, _ = PerfilRepartidor.objects.get_or_create(usuario=request.user)
        return Response(PerfilRepartidorSerializer(perfil).data)

    def put(self, request):
        entrada = MiUbicacionSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        perfil, _ = PerfilRepartidor.objects.get_or_create(usuario=request.user)
        activa = Asignacion.objects.filter(
            repartidor=request.user,
            pedido__estado__in=[Pedido.Estado.LISTO, Pedido.Estado.EN_CAMINO],
        ).order_by("-id").first()
        if entrada.validated_data.get("disponible") and activa:
            raise ValidationError("No puede marcarse disponible con una asignación activa")
        perfil.latitud = entrada.validated_data["latitud"]
        perfil.longitud = entrada.validated_data["longitud"]
        if "disponible" in entrada.validated_data:
            perfil.disponible = entrada.validated_data["disponible"]
        perfil.save()
        if activa:
            HistorialUbicacion.objects.create(
                asignacion=activa, latitud=perfil.latitud, longitud=perfil.longitud
            )
        return Response(PerfilRepartidorSerializer(perfil).data)


class PuntoRestauranteView(APIView):
    permission_classes = [rol_requerido("restaurante")]

    def put(self, request, restaurante_id):
        restaurante = get_object_or_404(Restaurante, pk=restaurante_id, dueno=request.user)
        entrada = CoordenadasSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        punto, _ = PuntoRestaurante.objects.update_or_create(
            restaurante=restaurante, defaults=entrada.validated_data
        )
        return Response(PuntoRestauranteSerializer(punto).data)


class AsignacionDetalleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pedido_id):
        pedido = get_object_or_404(Pedido.objects.filter(
            Q(cliente=request.user) | Q(restaurante__dueno=request.user) |
            Q(asignacion__repartidor=request.user)
        ).distinct(), pk=pedido_id)
        asignacion = get_object_or_404(Asignacion, pedido=pedido)
        return Response(AsignacionSerializer(asignacion).data)


class UbicacionAsignadaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pedido_id):
        pedido = get_object_or_404(Pedido.objects.filter(
            Q(cliente=request.user) | Q(restaurante__dueno=request.user) |
            Q(asignacion__repartidor=request.user)
        ).distinct(), pk=pedido_id)
        asignacion = get_object_or_404(Asignacion, pedido=pedido)
        perfil = get_object_or_404(PerfilRepartidor, usuario=asignacion.repartidor)
        return Response(PerfilRepartidorSerializer(perfil).data)