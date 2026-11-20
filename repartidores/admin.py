from django.contrib import admin
from repartidores.models import Asignacion, PerfilRepartidor, PuntoRestaurante


@admin.register(PuntoRestaurante)
class PuntoRestauranteAdmin(admin.ModelAdmin):
    list_display = ("id", "restaurante", "latitud", "longitud")


@admin.register(PerfilRepartidor)
class PerfilRepartidorAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "disponible", "latitud", "longitud", "actualizado_en")


@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    list_display = ("id", "pedido", "repartidor", "distancia_km", "fecha_asignacion")