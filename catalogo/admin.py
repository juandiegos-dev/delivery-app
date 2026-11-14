from django.contrib import admin

from catalogo.models import Producto, Restaurante

admin.site.register(Restaurante)
admin.site.register(Producto)
