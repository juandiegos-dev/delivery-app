from django.contrib import admin
from pedidos.models import Pedido, DetallePedido


class DetalleInline(admin.TabularInline):
    model = DetallePedido
    extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    inlines = [DetalleInline]
    list_display = (
        "id",
        "cliente",
        "restaurante",
        "estado",
        "total",
        "fecha_pedido",
    )