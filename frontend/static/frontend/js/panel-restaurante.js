const $ = id => document.getElementById(id);

let restauranteId = null;
let actualizando = false;

const lista = datos => Array.isArray(datos)
    ? datos : datos.results || [];

function mensaje(texto, correcto = true) {
    Delivery.mostrar($('resultado'), texto, correcto);
}

function boton(texto, clase, accion) {

    const b = document.createElement('button');

    b.type = 'button';
    b.className = clase + ' me-2 mb-2';
    b.textContent = texto;

    b.onclick = async () => {
        b.disabled = true;
        try {
            await accion();
        } catch (error) {
            mensaje(error.message, false);
        } finally {
            b.disabled = false;
        }
    };
    return b;
}

async function iniciar() {

    const perfil = await Delivery.perfil();
    if (!perfil) return;
    if (perfil.rol !== 'restaurante') {
        location.assign('/');
        return;
    }
    try {

        const restaurante = await Delivery.api(
            '/api/restaurantes/mi-restaurante/'
        );
        restauranteId = restaurante.id;
        $('nombreRestaurante').value = restaurante.nombre;
        $('direccionRestaurante').value = restaurante.direccion;
        $('administracion').classList.remove('d-none');
        await cargarProductos();
        await actualizarPedidos();

    } catch (error) {
        if (error.message.startsWith('HTTP 404:')) {
            mensaje('Registra primero tu restaurante.');
        } else {
            mensaje(error.message, false);
        }
    }
}

$('formRestaurante').onsubmit = async e => {
    e.preventDefault();
    try {
        const restaurante = await Delivery.api(
            restauranteId
                ? '/api/restaurantes/mi-restaurante/'
                : '/api/restaurantes/',
            {
                method: restauranteId ? 'PATCH' : 'POST',
                body: JSON.stringify({
                    nombre: $('nombreRestaurante').value.trim(),
                    direccion: $('direccionRestaurante').value.trim()
                })
            }
        );
        restauranteId = restaurante.id;
        $('administracion').classList.remove('d-none');
        mensaje('Restaurante guardado correctamente.');
        await cargarProductos();
        await actualizarPedidos();

    } catch (error) {
        mensaje(error.message, false);
    }
};

$('obtenerGPS').onclick = () => {
    if (!navigator.geolocation) {
        mensaje('GPS no disponible.', false);
        return;
    }

    navigator.geolocation.getCurrentPosition(
        posicion => {
            $('latitud').value = posicion.coords.latitude;
            $('longitud').value = posicion.coords.longitude;
        },
        error => mensaje(error.message, false),
        { enableHighAccuracy: true }
    );
};

$('formUbicacion').onsubmit = async e => {
    e.preventDefault();
    try {
        await Delivery.api(
            `/api/repartidores/restaurantes/${restauranteId}/ubicacion/`,
            {
                method: 'PUT',
                body: JSON.stringify({
                    latitud: Number($('latitud').value),
                    longitud: Number($('longitud').value)
                })
            }
        );

        mensaje('Ubicación guardada correctamente.');
    } catch (error) {
        mensaje(error.message, false);
    }
};

async function cargarProductos() {
    const datos = await Delivery.api('/api/productos/mis-productos/');
    $('tablaProductos').replaceChildren();
    for (const p of lista(datos)) {
        const fila = document.createElement('tr');
        for (const valor of [
            p.nombre,
            `S/ ${p.precio}`,
            p.disponible ? 'Disponible' : 'Inactivo'
        ]) {
            const celda = document.createElement('td');
            celda.textContent = valor;
            fila.append(celda);
        }

        const acciones = document.createElement('td');
        acciones.append(
            boton('Editar', 'btn btn-sm btn-outline-primary', () => {
                $('productoId').value = p.id;
                $('nombreProducto').value = p.nombre;
                $('precioProducto').value = p.precio;
                $('descripcionProducto').value = p.descripcion;
                $('disponibleProducto').checked = p.disponible;
                $('formProducto').scrollIntoView({
                    behavior: 'smooth'
                });
            }),

            boton(
                p.disponible ? 'Desactivar' : 'Activar',
                'btn btn-sm btn-outline-secondary',
                async () => {
                    await Delivery.api(`/api/productos/${p.id}/`, {
                        method: 'PATCH',
                        body: JSON.stringify({
                            disponible: !p.disponible
                        })
                    });
                    await cargarProductos();
                }
            ),

            boton('Eliminar', 'btn btn-sm btn-outline-danger', async () => {
                if (!confirm(`¿Eliminar ${p.nombre}?`)) return;
                await Delivery.api(`/api/productos/${p.id}/`, {
                    method: 'DELETE'
                });
                mensaje('Producto eliminado.');
                await cargarProductos();
            })
        );
        fila.append(acciones);
        $('tablaProductos').append(fila);
    }
}

function limpiarProducto() {
    $('formProducto').reset();
    $('productoId').value = '';
    $('disponibleProducto').checked = true;
}

$('limpiarProducto').onclick = limpiarProducto;
$('formProducto').onsubmit = async e => {
    e.preventDefault();
    const id = $('productoId').value;
    try {
        await Delivery.api(
            id
                ? `/api/productos/${id}/`
                : `/api/restaurantes/${restauranteId}/productos/`,
            {
                method: id ? 'PATCH' : 'POST',
                body: JSON.stringify({
                    nombre: $('nombreProducto').value.trim(),
                    precio: $('precioProducto').value,
                    descripcion: $('descripcionProducto').value.trim(),
                    disponible: $('disponibleProducto').checked
                })
            }
        );

        mensaje(id ? 'Producto actualizado.' : 'Producto registrado.');
        limpiarProducto();
        await cargarProductos();

    } catch (error) {
        mensaje(error.message, false);
    }
};

async function cambiarEstado(id, estado) {
    await Delivery.api(`/api/pedidos/${id}/estado/`, {
        method: 'PATCH',
        body: JSON.stringify({ estado })
    });

    mensaje('Estado del pedido actualizado.');
    await actualizarPedidos();
}

async function actualizarPedidos() {
    if (!restauranteId || actualizando) return;
    actualizando = true;
    try {
        const [pedidos, avisos] = await Promise.all([
            Delivery.api('/api/pedidos/recibidos/'),
            Delivery.api('/api/notificaciones/')
        ]);

        $('pedidos').replaceChildren();
        $('avisos').replaceChildren();
        for (const p of lista(pedidos)) {
            const col = document.createElement('div');
            col.className = 'col-md-6';
            const card = document.createElement('div');
            card.className = 'card card-body h-100';
            const titulo = document.createElement('h5');
            titulo.textContent = `Pedido #${p.id}`;
            const estado = document.createElement('p');
            estado.textContent = `Estado: ${p.estado}`;
            const total = document.createElement('p');
            total.textContent = `Total: S/ ${p.total}`;
            const direccion = document.createElement('p');
            direccion.textContent = p.direccion_entrega;
            card.append(titulo, estado, total, direccion);
            for (const detalle of p.detalles || []) {
                const item = document.createElement('small');
                item.textContent =
                    `${detalle.cantidad} × ${detalle.nombre_producto}`;
                card.append(item);
            }
            const acciones = document.createElement('div');
            acciones.className = 'mt-3';
            if (p.estado === 'PENDIENTE') {
                acciones.append(
                    boton('Aceptar', 'btn btn-success', () =>
                        cambiarEstado(p.id, 'ACEPTADO')
                    ),
                    boton('Rechazar', 'btn btn-danger', () => {
                        if (confirm('¿Rechazar este pedido?')) {
                            return cambiarEstado(p.id, 'RECHAZADO');
                        }
                    })
                );
            }

            if (p.estado === 'ACEPTADO') {
                acciones.append(
                    boton('Preparar pedido', 'btn btn-primary', () =>
                        cambiarEstado(p.id, 'EN_PREPARACION')
                    )
                );
            }

            if (p.estado === 'EN_PREPARACION') {
                acciones.append(
                    boton('Pedido listo', 'btn btn-success', () =>
                        cambiarEstado(p.id, 'LISTO')
                    )
                );
            }
            if (['EN_PREPARACION', 'LISTO', 'EN_CAMINO'].includes(p.estado)) {
                acciones.append(
                    boton('Registrar fallo', 'btn btn-outline-danger', async () => {
                        const motivo = prompt('Motivo del fallo:');
                        if (motivo === null) return;
                        if (motivo.trim().length < 8) {
                            throw new Error('Escribe al menos 8 caracteres.');
                        }
                        await Delivery.api(`/api/pedidos/${p.id}/fallido/`, {
                            method: 'POST',
                            body: JSON.stringify({ motivo })
                        });
                        await actualizarPedidos();
                    })
                );
            }
            const seguimiento = document.createElement('a');
            seguimiento.href = `/seguimiento/${p.id}/`;
            seguimiento.className = 'btn btn-outline-secondary mb-2';
            seguimiento.textContent = 'Seguimiento';
            acciones.append(seguimiento);
            card.append(acciones);
            col.append(card);
            $('pedidos').append(col);
        }

        if (!lista(pedidos).length) {
            $('pedidos').textContent = 'No hay pedidos recibidos.';
        }
        for (const n of lista(avisos)) {
            const li = document.createElement('li');
            li.className = 'list-group-item';
            li.textContent = n.mensaje;
            $('avisos').append(li);
        }

    } catch (error) {
        mensaje(error.message, false);
    } finally {
        actualizando = false;
    }
}
iniciar();
setInterval(() => {
    if (Delivery.token() && !document.hidden) {
        actualizarPedidos();
    }
}, 5000);