import os
from decimal import Decimal
from getpass import getpass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from catalogo.models import Restaurante, Producto
from pedidos.models import Pedido, DetallePedido, IncidenciaPedido
from pedidos.tarifas import calcular_tarifa_envio
from repartidores.models import (PuntoRestaurante, PerfilRepartidor,
                                 Asignacion, HistorialUbicacion)
from repartidores.services import distancia_km
from notificaciones.models import Notificacion

Usuario = get_user_model()
CLIENTES = [
    ('lucia.mendoza', 'Lucía', 'Mendoza'), ('mateo.rios', 'Mateo', 'Ríos'),
    ('valeria.salas', 'Valeria', 'Salas'), ('andres.paredes', 'Andrés', 'Paredes'),
    ('camila.vega', 'Camila', 'Vega'), ('sebastian.flores', 'Sebastián', 'Flores'),
    ('daniela.torres', 'Daniela', 'Torres'), ('gabriel.castro', 'Gabriel', 'Castro'),
    ('paola.navarro', 'Paola', 'Navarro'), ('nicolas.soto', 'Nicolás', 'Soto'),
]
REPARTIDORES = [
    ('marco.quispe', 'Marco', 'Quispe'), ('elena.arias', 'Elena', 'Arias'),
    ('bruno.lopez', 'Bruno', 'López'), ('sofia.reyes', 'Sofía', 'Reyes'),
    ('diego.ortiz', 'Diego', 'Ortiz'),
]
# Nombres comerciales, direcciones de referencia y GPS simulados.
CATALOGO = [
    ('el.dorado', 'Pollería El Dorado', 'Huánuco Centro', -9.9290, -76.2400, [
        ('¼ de pollo a la brasa', 'Con papas fritas, ensalada y cremas.', '18.00'),
        ('½ pollo a la brasa', 'Dos porciones con papas y ensalada.', '35.00'),
        ('Pollo entero', 'Pollo a la brasa, papas y ensalada familiar.', '65.00'),
        ('Salchipapa especial', 'Papas, salchicha y cremas.', '14.00'),
        ('Chaufa de pollo', 'Arroz salteado con pollo y huevo.', '16.00'),
        ('Chicha morada', 'Bebida de maíz morado de 1 litro.', '9.00'),
    ]),
    ('la.toscana', 'Pizzería La Toscana', 'Huánuco Centro', -9.9320, -76.2390, [
        ('Pizza americana', 'Jamón, mozzarella y salsa de tomate.', '28.00'),
        ('Pizza hawaiana', 'Jamón, piña y mozzarella.', '32.00'),
        ('Pizza pepperoni', 'Pepperoni y queso mozzarella.', '34.00'),
        ('Pizza vegetariana', 'Pimiento, champiñones y aceitunas.', '30.00'),
        ('Pan al ajo', 'Cuatro porciones de pan tostado.', '8.00'),
        ('Limonada', 'Limonada fresca de 1 litro.', '10.00'),
    ]),
    ('dragon.oriental', 'Chifa Dragón Oriental', 'Amarilis', -9.9410, -76.2420, [
        ('Chaufa de pollo', 'Arroz salteado con pollo, huevo y cebolla china.', '16.00'),
        ('Aeropuerto especial', 'Arroz y tallarines salteados con pollo.', '22.00'),
        ('Tallarín saltado', 'Tallarines con pollo y verduras.', '20.00'),
        ('Wantán frito', 'Seis wantanes con salsa agridulce.', '10.00'),
        ('Pollo tipakay', 'Pollo crocante con salsa agridulce.', '24.00'),
        ('Té de jazmín', 'Bebida caliente aromática.', '5.00'),
    ]),
    ('burger.house', 'Burger House', 'Huánuco Centro', -9.9300, -76.2350, [
        ('Hamburguesa clásica', 'Carne, lechuga, tomate y salsa de la casa.', '12.00'),
        ('Hamburguesa doble', 'Doble carne y queso cheddar.', '18.00'),
        ('Hamburguesa BBQ', 'Carne, tocino y salsa BBQ.', '19.00'),
        ('Alitas BBQ', 'Seis alitas con salsa BBQ.', '21.00'),
        ('Papas fritas', 'Porción de papas crocantes.', '7.00'),
        ('Gaseosa personal', 'Bebida de 500 ml.', '4.00'),
    ]),
    ('sazon.huanuquena', 'Sazón Huanuqueña', 'Pillco Marca', -9.9620, -76.2490, [
        ('Pachamanca', 'Carnes, papa, camote y choclo.', '25.00'),
        ('Picante de cuy', 'Cuy con salsa de ají y papas.', '35.00'),
        ('Locro de gallina', 'Sopa tradicional con papa y gallina.', '18.00'),
        ('Lomo saltado', 'Carne salteada, arroz y papas fritas.', '24.00'),
        ('Ají de gallina', 'Crema de ají amarillo con arroz.', '16.00'),
        ('Refresco de maracuyá', 'Bebida natural de 500 ml.', '6.00'),
    ]),
]


def correo(nombre):
    return f'{nombre}@delivery.test'


def cuenta_existente(nombre, rol):
    u = Usuario.objects.filter(username=nombre).first()
    if u is not None and (u.email != correo(nombre) or u.rol != rol
                          or u.is_staff or u.is_superuser):
        raise ValueError(f'Colisión de usuario: {nombre}. No se modificará.')
    if u is None and Usuario.objects.filter(email=correo(nombre)).exists():
        raise ValueError(f'Correo ya ocupado: {correo(nombre)}.')
    return u


def obtener_clave(nuevos):
    if not nuevos:
        return None
    print('Elige una contraseña local para las cuentas nuevas de demostración.')
    while True:
        clave = getpass('Contraseña (no visible): ')
        if clave != getpass('Confirma la contraseña: '):
            print('Las contraseñas no coinciden. Intenta nuevamente.')
            continue
        try:
            for nombre, nombres, apellidos, rol in nuevos:
                validate_password(clave, Usuario(username=nombre, email=correo(nombre),
                    first_name=nombres, last_name=apellidos, rol=rol))
            return clave
        except ValidationError as error:
            print('\n'.join(error.messages))


def cuenta(datos, clave):
    nombre, nombres, apellidos, rol = datos
    u = cuenta_existente(nombre, rol)
    if u is None:
        u = Usuario.objects.create_user(username=nombre, email=correo(nombre),
            password=clave, first_name=nombres, last_name=apellidos, rol=rol)
    return u


def avisar(usuario, pedido, tipo, mensaje):
    Notificacion.objects.create(destinatario=usuario, pedido=pedido,
                                tipo=tipo, mensaje=mensaje)


def cargar():
    datos = ([(*c, 'cliente') for c in CLIENTES]
             + [(r[0], r[1], '', 'restaurante') for r in CATALOGO]
             + [(*r, 'repartidor') for r in REPARTIDORES])
    nuevos = [d for d in datos if cuenta_existente(d[0], d[3]) is None]
    clave = obtener_clave(nuevos)
    with transaction.atomic():
        usuarios = {d[0]: cuenta(d, clave) for d in datos}
        restaurantes, menus, perfiles = [], [], []
        for nombre, negocio, zona, lat, lon, platos in CATALOGO:
            r, _ = Restaurante.objects.get_or_create(dueno=usuarios[nombre],
                defaults={'nombre': negocio, 'direccion': zona + ', Huánuco'})
            PuntoRestaurante.objects.get_or_create(restaurante=r,
                defaults={'latitud': lat, 'longitud': lon})
            restaurantes.append(r)
            menu = []
            for plato, descripcion, precio in platos:
                p, _ = Producto.objects.get_or_create(restaurante=r, nombre=plato,
                    defaults={'descripcion': descripcion, 'precio': Decimal(precio),
                              'disponible': True})
                menu.append(p)
            menus.append(menu)
        for i, (nombre, _, _) in enumerate(REPARTIDORES):
            perfil, _ = PerfilRepartidor.objects.get_or_create(usuario=usuarios[nombre],
                defaults={'latitud': -9.930 - i * .002,
                          'longitud': -76.240 + i * .001, 'disponible': True})
            perfiles.append(perfil)

        E = Pedido.Estado
        estados = [E.ENTREGADO] * 8 + [E.CANCELADO, E.RECHAZADO, E.FALLIDO,
            E.PENDIENTE, E.ACEPTADO, E.EN_PREPARACION, E.PENDIENTE, E.ACEPTADO,
            E.EN_PREPARACION, E.LISTO, E.EN_CAMINO, E.EN_CAMINO]
        creados = 0
        for i, estado in enumerate(estados):
            cliente = usuarios[CLIENTES[i % len(CLIENTES)][0]]
            j = i % len(restaurantes)
            r = restaurantes[j]
            marca = f'[DEMO-DELIVERY-{i+1:02d}]'
            if Pedido.objects.filter(cliente=cliente, observaciones__startswith=marca).exists():
                continue
            platos = [menus[j][i % 6], menus[j][(i + 2) % 6]]
            cantidades = [1 + i % 2, 1]
            subtotal = sum((p.precio * c for p, c in zip(platos, cantidades)), Decimal('0.00'))
            envio = calcular_tarifa_envio(r)
            p = Pedido.objects.create(cliente=cliente, restaurante=r,
                direccion_entrega=['Huánuco Centro', 'Amarilis', 'Pillco Marca'][i % 3],
                observaciones=marca + ' Entregar en recepción.', estado=estado,
                subtotal=subtotal, costo_envio=envio, total=subtotal + envio,
                entregado_en=timezone.now() if estado == E.ENTREGADO else None)
            for producto, cantidad in zip(platos, cantidades):
                DetallePedido.objects.create(pedido=p, producto=producto,
                    nombre_producto=producto.nombre, cantidad=cantidad,
                    precio_unitario=producto.precio, subtotal=producto.precio * cantidad)
            avisar(r.dueno, p, 'NUEVO_PEDIDO', f'Nuevo pedido #{p.pk}.')
            avisar(cliente, p, 'ESTADO', f'Pedido #{p.pk}: {p.get_estado_display()}.')
            if estado in (E.CANCELADO, E.FALLIDO):
                cancelado = estado == E.CANCELADO
                IncidenciaPedido.objects.create(pedido=p,
                    actor=cliente if cancelado else r.dueno,
                    tipo='CANCELACION' if cancelado else 'FALLO',
                    motivo='Cambio de planes del cliente.' if cancelado else 'Insumos agotados.')
            if estado in (E.ENTREGADO, E.LISTO, E.EN_CAMINO):
                perfil = perfiles[i % len(perfiles)] if estado == E.ENTREGADO else perfiles[i-17]
                # No ocupar un repartidor que ya esté atendiendo un pedido real.
                if estado != E.ENTREGADO and not perfil.disponible:
                    raise ValueError(f'{perfil.usuario.username} no está disponible. '
                                     'Termina su reparto antes de cargar este lote.')
                punto = r.punto_gps
                lat = perfil.latitud if perfil.latitud is not None else punto.latitud
                lon = perfil.longitud if perfil.longitud is not None else punto.longitud
                a = Asignacion.objects.create(pedido=p, repartidor=perfil.usuario,
                    distancia_km=Decimal(str(distancia_km(punto.latitud, punto.longitud,
                        lat, lon))).quantize(Decimal('0.01')))
                avisar(perfil.usuario, p, 'ASIGNACION', f'Pedido #{p.pk} asignado.')
                avisar(cliente, p, 'ASIGNACION', f'Repartidor asignado al pedido #{p.pk}.')
                if estado in (E.ENTREGADO, E.EN_CAMINO):
                    for paso in (0, 1, 2):
                        HistorialUbicacion.objects.create(asignacion=a,
                            latitud=lat + paso * .0003, longitud=lon + paso * .0002)
                if estado != E.ENTREGADO:
                    perfil.disponible = False
                    perfil.save(update_fields=['disponible', 'actualizado_en'])
            creados += 1
    print('\nDatos de demostración preparados correctamente.')
    print('Lote: 10 clientes, 5 restaurantes, 30 productos, 5 repartidores y 20 pedidos.')
    print(f'Pedidos nuevos en esta ejecución: {creados}.')
    print('Cuentas sugeridas para ingresar: lucia.mendoza / el.dorado / marco.quispe')
    print('Las cuentas existentes conservan su contraseña.')


if __name__ == '__main__':
    try:
        cargar()
    except (ValueError, ValidationError) as error:
        raise SystemExit(f'Carga cancelada: {error}')
