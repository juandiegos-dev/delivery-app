# Delivery App — Plataforma de Delivery de Comida

**Universidad de Huánuco | Ingeniería de Sistemas e Informática**

**Ingeniería de Software — Hito Final 2026 — Grupo 1**

## 1. Descripción del proyecto

Delivery App es una aplicación web que permite conectar clientes,
restaurantes y repartidores mediante una plataforma centralizada
para la gestión de pedidos de comida.

El sistema permite consultar restaurantes, gestionar productos,
realizar pedidos, calcular tarifas de envío según la demanda,
asignar repartidores según su cercanía, consultar ubicaciones GPS
y recibir notificaciones sobre el estado de los pedidos.

El proyecto fue desarrollado colaborativamente por cinco integrantes,
utilizando Git y GitHub como herramientas de control de versiones.

## 2. Tecnologías utilizadas

| Tecnología | Versión o descripción |
|---|---|
| Python | 3.12 |
| Django | 5.1.4 |
| Django REST Framework | 3.15.2 |
| SQLite | Base de datos relacional local |
| HTML | Estructura de interfaces |
| CSS | Diseño de interfaces |
| JavaScript | Interactividad y consumo de API |
| Geolocalización GPS | Seguimiento de repartidores |
| Git | Control de versiones |
| GitHub | Repositorio colaborativo |
| Visual Studio Code | Entorno de desarrollo |

## 3. Funcionalidades del sistema

### Cliente

- Registro de cuenta.
- Inicio y cierre de sesión.
- Consulta de restaurantes.
- Visualización de menús y productos disponibles.
- Creación de pedidos.
- Consulta de tarifas de envío.
- Consulta del historial de pedidos.
- Seguimiento de estados.
- Cancelación de pedidos según las reglas del negocio.
- Seguimiento de la ubicación del repartidor asignado.
- Recepción de notificaciones.

### Restaurante

- Registro e inicio de sesión.
- Registro y consulta de su restaurante.
- Creación, consulta, actualización y eliminación de productos.
- Gestión de disponibilidad de productos.
- Recepción de pedidos.
- Aceptación y rechazo de pedidos.
- Actualización de estados de preparación.
- Registro de ubicación GPS.
- Cancelación de pedidos autorizados.
- Registro de incidencias y pedidos fallidos.
- Recepción de notificaciones.

### Repartidor

- Registro e inicio de sesión.
- Registro y actualización de ubicación GPS.
- Control de disponibilidad.
- Recepción de pedidos asignados.
- Consulta del pedido asignado.
- Inicio del reparto.
- Confirmación de entrega.
- Actualización del recorrido GPS.
- Recepción de notificaciones.

### Funcionalidades generales

- Autenticación mediante token.
- Control de permisos según el rol del usuario.
- Validación de datos.
- Asignación automática de repartidores mediante Haversine.
- Cálculo de tarifas dinámicas según demanda.
- Gestión de incidencias.
- Notificaciones internas.
- Protección de contraseñas mediante hash.
- Pruebas automatizadas.

## 4. Arquitectura del sistema

El proyecto utiliza una arquitectura cliente-servidor.

La interfaz web consume los servicios proporcionados por una API REST
desarrollada con Django REST Framework.

El backend contiene la lógica del negocio, las validaciones,
los permisos y la comunicación con la base de datos SQLite
mediante el ORM de Django.

```text
Usuario
   |
Interfaz web (HTML, CSS y JavaScript)
   |
API REST (Django REST Framework)
   |
Lógica del negocio (Django)
   |
ORM de Django
   |
Base de datos SQLite
```

## 5. Estructura del proyecto

```text
delivery-app/
|
|-- accesos/
|   |-- models.py
|   |-- serializers.py
|   |-- views.py
|   |-- urls.py
|   |-- tests.py
|   |-- migrations/
|
|-- catalogo/
|   |-- models.py
|   |-- serializers.py
|   |-- views.py
|   |-- urls.py
|   |-- migrations/
|
|-- pedidos/
|   |-- models.py
|   |-- serializers.py
|   |-- services.py
|   |-- tarifas.py
|   |-- cancelaciones.py
|   |-- views.py
|   |-- urls.py
|   |-- migrations/
|
|-- repartidores/
|   |-- models.py
|   |-- services.py
|   |-- entregas.py
|   |-- vistas_gps.py
|   |-- urls.py
|   |-- migrations/
|
|-- notificaciones/
|   |-- models.py
|   |-- services.py
|   |-- views.py
|   |-- urls.py
|   |-- migrations/
|
|-- frontend/
|-- config/
|-- docs/
|   |-- Manual_Instalacion_Ejecucion.docx
|   |-- Hito_Final_Grupo1.docx
|
|-- crear_base_datos.py
|-- cargar_datos_prueba.py
|-- manage.py
|-- requirements.txt
|-- README.md
|-- .gitignore
```

## 6. Módulos del sistema

| Módulo | Responsabilidad |
|---|---|
| Accesos | Registro, autenticación y gestión de usuarios |
| Catálogo | Gestión de restaurantes, productos y menús |
| Pedidos | Creación, estados, tarifas, cancelaciones e incidencias |
| Repartidores | Asignación, GPS, seguimiento y confirmación de entregas |
| Notificaciones | Comunicación de eventos relacionados con los pedidos |
| Frontend | Interfaz web e interacción con la API REST |

## 7. Requisitos de instalación

Antes de instalar el proyecto, se requiere:

- Python 3.12.
- Git.
- Visual Studio Code o cualquier editor de código.
- Navegador web actualizado.
- Conexión a Internet para descargar las dependencias.
- Permisos de ubicación del navegador para las funciones GPS.

SQLite se encuentra integrado con Python y no requiere instalar
un servidor de base de datos adicional.

## 8. Instalación y ejecución

Las siguientes instrucciones están orientadas a Windows
utilizando PowerShell.

### 8.1. Clonar el repositorio

```powershell
git clone https://github.com/juandiegos-dev/delivery-app.git
cd delivery-app
```

### 8.2. Seleccionar la rama principal

```powershell
git switch main
```

### 8.3. Crear el entorno virtual

```powershell
py -3.12 -m venv .venv312
```

### 8.4. Activar el entorno virtual

```powershell
.\.venv312\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, ejecutar:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv312\Scripts\Activate.ps1
```

### 8.5. Instalar las dependencias

```powershell
python -m pip install -r requirements.txt
```

### 8.6. Configurar la clave privada de Django

Por seguridad, el proyecto no almacena la clave privada de Django
directamente en el código fuente.

La clave debe configurarse mediante una variable de entorno:

```powershell
$env:DJANGO_SECRET_KEY = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

La variable permanecerá disponible durante la sesión actual
de PowerShell.

Si se abre una nueva terminal, será necesario volver a configurar
la variable antes de ejecutar Django.

Para una instalación permanente, se recomienda conservar una clave
propia y segura en la configuración local del entorno.

No compartir ni subir esta clave al repositorio.

### 8.7. Crear la base de datos

Ejecutar el script de creación de la base de datos:

```powershell
python crear_base_datos.py
```

El script ejecuta las migraciones de Django y crea las tablas,
relaciones y restricciones correspondientes.

También es posible ejecutar directamente:

```powershell
python manage.py migrate
```

### 8.8. Cargar datos de demostración

```powershell
python cargar_datos_prueba.py
```

El script genera un conjunto de datos ficticios para demostrar
las funcionalidades del sistema.

| Información | Cantidad |
|---|---:|
| Clientes | 10 |
| Restaurantes | 5 |
| Productos | 30 |
| Repartidores | 5 |
| Pedidos | 20 |

También se generan:

- Notificaciones.
- Asignaciones de repartidores.
- Incidencias de pedidos.
- Coordenadas GPS simuladas.
- Historiales de ubicación.
- Pedidos en diferentes estados.

Durante la primera ejecución, el script solicitará una contraseña
local para las cuentas nuevas.

La contraseña deberá cumplir las validaciones de seguridad
establecidas por Django.

No se incluyen contraseñas reales en el código fuente.

Los datos generados corresponden únicamente a escenarios ficticios
de demostración académica.

### 8.9. Verificar la configuración

```powershell
python manage.py check
```

### 8.10. Iniciar el servidor

```powershell
python manage.py runserver
```

Ingresar desde el navegador:

http://127.0.0.1:8000/

Para detener el servidor:

```text
Ctrl + C
```

## 9. Cuentas de demostración

Las siguientes cuentas se generan mediante el script
cargar_datos_prueba.py.

| Usuario | Rol |
|---|---|
| lucia.mendoza | Cliente |
| mateo.rios | Cliente |
| valeria.salas | Cliente |
| el.dorado | Restaurante |
| la.toscana | Restaurante |
| dragon.oriental | Restaurante |
| burger.house | Restaurante |
| sazon.huanuquena | Restaurante |
| marco.quispe | Repartidor |
| elena.arias | Repartidor |
| bruno.lopez | Repartidor |
| sofia.reyes | Repartidor |
| diego.ortiz | Repartidor |

La contraseña corresponde a la ingresada durante la ejecución
del script de datos.

Las cuentas existentes conservan su contraseña.

## 10. Restaurantes de demostración

| Restaurante | Tipo de comida |
|---|---|
| Pollería El Dorado | Pollos a la brasa |
| Pizzería La Toscana | Pizzas |
| Chifa Dragón Oriental | Comida oriental |
| Burger House | Hamburguesas y comida rápida |
| Sazón Huanuqueña | Comida regional |

Cada restaurante incluye seis productos con sus respectivas
descripciones, precios y disponibilidad.

Los nombres comerciales y las ubicaciones utilizadas son ficticios
o simulados para fines académicos.

## 11. Rutas principales de la interfaz

| Ruta | Descripción |
|---|---|
| / | Página principal |
| /login/ | Inicio de sesión |
| /registro/ | Registro de usuarios |
| /restaurantes/ | Catálogo de restaurantes |
| /mis-pedidos/ | Pedidos del cliente |
| /panel-restaurante/ | Panel del restaurante |
| /panel-repartidor/ | Panel del repartidor |
| /ubicacion/ | Gestión de ubicación GPS |
| /seguimiento/{pedido_id}/ | Seguimiento de pedidos |
| /admin/ | Administración de Django |

## 12. Endpoints de la API REST

### Accesos

| Método | Endpoint | Descripción |
|---|---|---|
| POST | /api/auth/registro/ | Registro de usuarios |
| POST | /api/auth/login/ | Autenticación y generación de token |
| GET | /api/auth/yo/ | Consulta del usuario autenticado |

### Catálogo

| Endpoint | Descripción |
|---|---|
| /api/restaurantes/ | Gestión y listado de restaurantes |
| /api/restaurantes/mi-restaurante/ | Restaurante del propietario |
| /api/productos/mis-productos/ | Productos del propietario |
| /api/restaurantes/{id}/menu/ | Menú del restaurante |
| /api/restaurantes/{id}/productos/ | Registro de productos |
| /api/productos/{id}/ | Consulta, modificación y eliminación |

### Pedidos

| Endpoint | Descripción |
|---|---|
| /api/pedidos/ | Creación de pedidos |
| /api/pedidos/mis-pedidos/ | Pedidos del cliente |
| /api/pedidos/recibidos/ | Pedidos del restaurante |
| /api/pedidos/{id}/ | Detalle del pedido |
| /api/pedidos/{id}/estado/ | Actualización del estado |
| /api/pedidos/{id}/cancelar/ | Cancelación del pedido |
| /api/pedidos/{id}/fallido/ | Registro de pedido fallido |
| /api/pedidos/cotizar/{id}/ | Cotización de envío |

### Repartidores

| Endpoint | Descripción |
|---|---|
| /api/repartidores/mi-ubicacion/ | Ubicación del repartidor |
| /api/repartidores/mis-asignaciones/ | Pedidos asignados |
| /api/repartidores/restaurantes/{id}/ubicacion/ | GPS del restaurante |
| /api/repartidores/pedidos/{id}/asignacion/ | Repartidor asignado |
| /api/repartidores/pedidos/{id}/ubicacion/ | Ubicación asignada |
| /api/repartidores/pedidos/{id}/ruta/ | Consulta del recorrido GPS |
| /api/repartidores/pedidos/{id}/iniciar-reparto/ | Inicio del reparto |
| /api/repartidores/pedidos/{id}/confirmar-entrega/ | Confirmación de entrega |

### Notificaciones

| Método | Endpoint | Descripción |
|---|---|---|
| GET | /api/notificaciones/ | Notificaciones del usuario |

Los endpoints protegidos requieren autenticación y los permisos
correspondientes al rol del usuario.

## 13. Autenticación

El sistema utiliza TokenAuthentication de Django REST Framework.

Después de iniciar sesión, la API devuelve un token de autenticación.

Las solicitudes a rutas protegidas deben incluir la cabecera:

```text
Authorization: Token <token_del_usuario>
```

Los permisos del backend restringen las operaciones según el rol
y la participación del usuario en cada pedido.

## 14. Estados de los pedidos

| Estado | Descripción |
|---|---|
| PENDIENTE | Pedido registrado y pendiente de revisión |
| ACEPTADO | Pedido aceptado por el restaurante |
| RECHAZADO | Pedido rechazado por el restaurante |
| EN_PREPARACION | Pedido en preparación |
| LISTO | Pedido preparado para reparto |
| EN_CAMINO | Pedido en proceso de entrega |
| ENTREGADO | Entrega confirmada |
| CANCELADO | Pedido cancelado |
| FALLIDO | Pedido con una incidencia que impide su finalización |

Flujo principal:

```text
PENDIENTE
    |
ACEPTADO
    |
EN_PREPARACION
    |
LISTO
    |
EN_CAMINO
    |
ENTREGADO
```

Las cancelaciones, rechazos y fallos se gestionan de acuerdo
con las reglas de transición y permisos implementados.

## 15. Asignación automática de repartidores

Cuando un pedido cambia al estado LISTO, el sistema consulta
los repartidores disponibles que cuentan con coordenadas GPS.

Mediante la fórmula de Haversine, se calcula la distancia
entre el restaurante y cada repartidor disponible.

Se selecciona al repartidor más cercano y se registra
la asignación correspondiente.

El repartidor permanece ocupado durante la entrega y vuelve
a estar disponible al confirmar su finalización.

## 16. Tarifas dinámicas

El costo del envío se determina según la cantidad de pedidos
activos del restaurante.

| Pedidos activos | Factor | Costo de envío |
|---|---:|---:|
| De 0 a 4 | 1.0 | S/ 5.00 |
| De 5 a 9 | 1.5 | S/ 7.50 |
| 10 o más | 2.0 | S/ 10.00 |

La tarifa se calcula durante la creación del pedido.

```text
Subtotal = Suma de los precios por cantidad
Total = Subtotal + Costo de envío
```

Los pedidos en estados terminales no se consideran activos
para el cálculo de la tarifa.

## 17. Base de datos

El proyecto utiliza SQLite y el ORM de Django.

Las entidades principales son:

- Usuario.
- Restaurante.
- Producto.
- Pedido.
- DetallePedido.
- IncidenciaPedido.
- PuntoRestaurante.
- PerfilRepartidor.
- Asignacion.
- HistorialUbicacion.
- Notificacion.

Las relaciones y restricciones se encuentran definidas
en los modelos y migraciones de cada aplicación.

### Scripts incluidos

| Archivo | Función |
|---|---|
| crear_base_datos.py | Ejecuta las migraciones y prepara la base de datos |
| cargar_datos_prueba.py | Genera información ficticia relacionada para demostraciones |

El archivo db.sqlite3 se genera localmente y no se incluye
en el repositorio.

## 18. Pruebas automatizadas

El proyecto incorpora pruebas automatizadas mediante Django TestCase
y las herramientas de pruebas de Django REST Framework.

Para ejecutar todas las pruebas:

```powershell
python manage.py test -v 2
```

### Pruebas por módulo

```powershell
python manage.py test accesos -v 2
python manage.py test catalogo -v 2
python manage.py test pedidos -v 2
python manage.py test repartidores -v 2
python manage.py test notificaciones -v 2
python manage.py test frontend -v 2
```

### Distribución de pruebas

| Módulo | Cantidad |
|---|---:|
| Accesos | 8 |
| Catálogo | 15 |
| Pedidos | 30 |
| Repartidores | 14 |
| Notificaciones | 3 |
| Frontend | 3 |
| Total | 73 |

Las pruebas incluyen casos normales, datos inválidos,
condiciones límite, autenticación, permisos e integración
entre módulos.

Los resultados de ejecución y las evidencias manuales
se documentan en el informe final del proyecto.

## 19. Seguridad

El sistema incorpora las siguientes medidas:

- Autenticación mediante token.
- Contraseñas almacenadas mediante hash.
- Validación de contraseñas.
- Validación de datos recibidos mediante serializadores.
- Permisos según el rol del usuario.
- Protección de pedidos y notificaciones privadas.
- Restricción de operaciones sobre recursos de otros usuarios.
- Validación de coordenadas geográficas.
- Uso de variables de entorno para la clave privada de Django.
- Exclusión de archivos locales y sensibles mediante .gitignore.

El proyecto está configurado para desarrollo y demostración académica.

Antes de utilizarlo en producción, se requiere configurar HTTPS,
desactivar DEBUG y establecer los parámetros de seguridad
correspondientes al entorno de despliegue.

## 20. Limitaciones del sistema

- La asignación automática requiere repartidores disponibles
  y coordenadas GPS registradas.
- Si no existe un repartidor disponible al cambiar el pedido
  a LISTO, la asignación automática puede quedar pendiente.
- El cálculo Haversine representa una distancia geográfica
  aproximada y no una distancia real por calles.
- El seguimiento representa coordenadas registradas y no incluye
  estimación avanzada del tiempo de llegada.
- La geolocalización depende de los permisos del navegador.
- SQLite está orientado al entorno local de demostración.

Las limitaciones relacionadas con los requerimientos se detallan
en la matriz de trazabilidad del informe final.

## 21. Integrantes del Grupo 1

| Integrante | Usuario de GitHub | Responsabilidades principales |
|---|---|---|
| Diego Sabino Juan Clin | juandiegos-dev | Catálogo, creación de pedidos, integración e interfaz |
| Masgo Viera Francklin | 2024110730-hue | Modelos, asignación y gestión de entregas |
| Gomero Cespedes Yazmin Zamira | 2024110779-byte | Estados, gestión y cancelación de pedidos |
| Gayoso Remigio Freddy | gayosofreddy79-max | Productos, tarifas, notificaciones e incidencias |
| Ureta Soto Víctor Fernando | 2024110709-sys | Autenticación, permisos y seguimiento GPS |

Todos los integrantes participaron mediante ramas individuales,
commits y Pull Requests.

## 22. Control de versiones

El proyecto fue desarrollado utilizando Git y GitHub.

La rama principal contiene los módulos integrados.

Los integrantes desarrollaron sus funcionalidades en ramas
individuales y utilizaron Pull Requests para incorporar
sus cambios al proyecto.

Repositorio:

https://github.com/juandiegos-dev/delivery-app

Historial de commits:

https://github.com/juandiegos-dev/delivery-app/commits/main/

Pull Requests:

https://github.com/juandiegos-dev/delivery-app/pulls

Contribuciones:

https://github.com/juandiegos-dev/delivery-app/graphs/contributors

## 23. Documentación

La carpeta docs/ está destinada a contener los siguientes documentos
correspondientes a la entrega final:

- Manual de instalación y ejecución.
- Informe final del Grupo 1.

El informe final incluye:

- Análisis y diseño del sistema.
- Requerimientos funcionales y no funcionales.
- Diagramas UML.
- Modelo entidad-relación.
- Diccionario de datos.
- Informes individuales.
- Matriz de trazabilidad.
- Registro de cambios.
- Casos de prueba.
- Evaluación de contribuciones.
- Evidencias del proyecto.

## 24. Información académica

- Universidad: Universidad de Huánuco.
- Escuela profesional: Ingeniería de Sistemas e Informática.
- Curso: Ingeniería de Software.
- Docente: Mg. Omar Sulca Correa.
- Grupo: 1.
- Proyecto: Plataforma de Delivery de Comida.
- Entrega: Hito Final.
- Año: 2026.

---

Proyecto desarrollado con fines académicos por estudiantes
de Ingeniería de Sistemas e Informática de la Universidad de Huánuco.
