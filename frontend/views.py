from django.shortcuts import render

# Create your views here.

def inicio(request):
    return render(request, "frontend/inicio.html")


def login(request):
    return render(request, "frontend/login.html")


def registro(request):
    return render(request, "frontend/registro.html")


def restaurantes(request):
    return render(request, "frontend/restaurantes.html")


def mis_pedidos(request):
    return render(request, "frontend/mis_pedidos.html")


def panel_restaurante(request):
    return render(request, "frontend/panel_restaurante.html")


def panel_repartidor(request):
    return render(request, "frontend/panel_repartidor.html")


def ubicacion(request):
    return render(request, "frontend/ubicacion.html")


def seguimiento(request, pedido_id):
    # Página vacía de datos: el endpoint REST validará token y permisos.
    return render(request, "frontend/seguimiento.html", {"pedido_id": pedido_id})