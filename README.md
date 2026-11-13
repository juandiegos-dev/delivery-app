
# 🍔 Plataforma de Delivery de Comida

**Universidad de Huánuco — Ingeniería de Software (2026)**

Sistema de delivery de comida desarrollado con Python, Django y Django REST Framework, que permite conectar clientes, restaurantes y repartidores.

Este proyecto es desarrollado de manera colaborativa por cinco integrantes, utilizando Git y GitHub para el control de versiones.

## 🛠️ Tecnologías utilizadas

- Python
- Django
- Django REST Framework
- SQLite (base de datos local)
- Git y GitHub
- Visual Studio Code

## 📁 Estructura del proyecto

```text
delivery-app/
│
├── accesos/             # Registro, autenticación y usuarios
├── catalogo/            # Restaurantes, menús y productos
├── pedidos/             # Registro y gestión de pedidos
├── config/              # Configuración principal de Django
├── manage.py            # Administración del proyecto
├── requirements.txt     # Dependencias de Python
├── .gitignore
└── README.md
```

## 🚀 Instalación inicial (primera vez)

Cada integrante debe realizar estos pasos en su propia computadora.

### 1. Clonar el repositorio desde VS Code

1. Abrir Visual Studio Code.
2. Presionar `Ctrl + Shift + P`.
3. Buscar `Git: Clone`.
4. Pegar el enlace:

```text
https://github.com/juandiegos-dev/delivery-app.git
```

5. Seleccionar una carpeta donde guardar el proyecto.
6. Presionar **Open** para abrirlo.

También se puede clonar desde la terminal:

```powershell
git clone https://github.com/juandiegos-dev/delivery-app.git
cd delivery-app
```

### 2. Configurar Git

Cada integrante debe configurar su propio nombre y correo vinculado a GitHub.

```powershell
git config --global user.name "Tu Nombre"
git config --global user.email "tu_correo@gmail.com"
```

### 3. Crear el entorno virtual

```powershell
python -m venv env
```

Activar el entorno:

```powershell
.\env\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\env\Scripts\Activate.ps1
```

Cuando el entorno esté activado aparecerá `(env)` al inicio de la terminal.

**Importante:** cada integrante crea su propio `env`. Esta carpeta no se sube a GitHub.

### 4. Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

### 5. Preparar la base de datos

```powershell
python manage.py migrate
```

### 6. Ejecutar el servidor

```powershell
python manage.py runserver
```

Abrir en el navegador:

http://127.0.0.1:8000/

Para detener el servidor, presionar `Ctrl + C`.

---

## 🌿 Ramas de trabajo

Cada integrante debe trabajar en su propia rama, sin modificar directamente `main`.

| Integrante | Rama | Responsabilidad |
|---|---|---|
| Diego Sabino | `feature/catalogo` | Consulta de restaurantes y menús |
| Francklin Masgo | `feature/modelos` | Modelos y base de datos |
| Víctor Ureta | `feature/acceso` | Registro y autenticación |
| Yazmin Gomero | `feature/pedidos` | Gestión de pedidos |
| Freddy Gayoso | `feature/crud-productos` | CRUD de productos |

### Crear una rama por primera vez

Primero actualizar la rama principal:

```powershell
git switch main
git pull origin main
```

Después crear la rama correspondiente. Por ejemplo:

```powershell
git switch -c feature/catalogo
```

Publicarla en GitHub:

```powershell
git push -u origin feature/catalogo
```

**Nota:** reemplazar `feature/catalogo` por la rama asignada. Si la rama ya existe, cambiar a ella en lugar de crearla nuevamente.

---

## 💻 Trabajo diario

Cada vez que un integrante vaya a programar, debe realizar lo siguiente.

### 1. Abrir el proyecto y activar el entorno

```powershell
.\env\Scripts\Activate.ps1
```

### 2. Entrar a su rama

Ejemplo:

```powershell
git switch feature/catalogo
```

### 3. Descargar actualizaciones de su rama

```powershell
git pull --ff-only
```

### 4. Programar

Modificar los archivos correspondientes a su módulo y guardar con `Ctrl + S`.

### 5. Revisar los archivos modificados

```powershell
git status
```

### 6. Preparar los cambios

```powershell
git add .
```

### 7. Crear un commit

```powershell
git commit -m "Agrega funcionalidad del catalogo"
```

### 8. Subir los cambios a GitHub

```powershell
git push
```

### Resumen de comandos diarios

```powershell
git status
git add .
git commit -m "Descripcion del avance"
git push
```

Se recomienda realizar commits pequeños, con mensajes que expliquen claramente qué se implementó.

---

## 🔄 Actualizar la rama con cambios de los compañeros

Cuando los cambios de otros integrantes ya estén integrados en `main`, se pueden incorporar a la rama personal.

Primero guardar o confirmar los cambios locales pendientes.

```powershell
git switch main
git pull origin main
```

Volver a la rama personal:

```powershell
git switch feature/catalogo
```

Integrar las actualizaciones:

```powershell
git merge main
```

Si aparecen conflictos, resolverlos antes de continuar.

Finalmente:

```powershell
git push
```

**No es necesario volver a clonar el repositorio.**

---

## 🔀 Pull Requests

Cuando un integrante termine una funcionalidad:

1. Realizar `git add`, `git commit` y `git push`.
2. Entrar al repositorio en GitHub.
3. Seleccionar **Pull requests**.
4. Presionar **New pull request**.
5. Seleccionar `base: main`.
6. Seleccionar `compare: feature/nombre-rama`.
7. Presionar **Create pull request**.
8. Solicitar la revisión de otro integrante.
9. Integrar los cambios con **Merge pull request** cuando estén correctos.

Los Pull Requests permiten integrar el trabajo de manera organizada y conservar evidencia de la colaboración.

---

## 🧪 Pruebas del proyecto

Antes de subir una funcionalidad, comprobar que Django no presente errores:

```powershell
python manage.py check
```

Ejecutar las pruebas automatizadas existentes:

```powershell
python manage.py test
```

También se realizarán pruebas manuales para verificar los flujos principales de cada módulo.

## 📋 Hito 2 — Requisitos

Para cumplir con el segundo hito de Ingeniería de Software se debe presentar:

- Un avance del proyecto igual o superior al 30 %, sustentado en una tabla de funcionalidades.
- Al menos dos módulos funcionales a nivel básico.
- Un repositorio GitHub actualizado.
- Commits individuales de los cinco integrantes.
- Un informe grupal en Word con los avances individuales.
- Evidencias de funcionamiento y pruebas.

Se recomiendan al menos **3 commits por integrante, realizados en 2 días diferentes**.

Cada módulo debe contar con un mínimo de cinco pruebas manuales:

- Dos casos normales.
- Dos casos con datos inválidos.
- Un caso con datos límite.

## ⚠️ Reglas de colaboración

1. Cada integrante trabaja desde su propia cuenta de GitHub.
2. No realizar modificaciones directamente en `main`.
3. No subir la carpeta `env/`.
4. No subir contraseñas ni archivos `.env` con información privada.
5. Mantener actualizado `requirements.txt` cuando se agreguen dependencias.
6. Utilizar mensajes de commit descriptivos.
7. Revisar los Pull Requests antes de integrarlos.
8. No modificar los modelos o configuraciones de otro integrante sin coordinación.
9. Registrar las pruebas y capturas del trabajo realizado.
10. Mantener la documentación actualizada.

---

## 👥 Integrantes

| Integrante | Responsabilidad |
|---|---|
| Diego Sabino Juan Clint | Backend — Catálogo y representante |
| Masgo Viera Francklin | Backend — Modelos de datos |
| Ureta Soto Víctor Fernando | Backend — Acceso |
| Gomero Céspedes Yazmin Zamira | Backend — Pedidos |
| Gayoso Remigio Freddy | Backend — CRUD de productos |

## 📚 Información académica

**Universidad:** Universidad de Huánuco  
**Escuela profesional:** Ingeniería de Sistemas e Informática  
**Curso:** Ingeniería de Software  
**Docente:** Mg. Omar Sulca Correa  
**Proyecto:** Análisis y diseño de una plataforma de delivery de comida  
**Año:** 2026

---

**Repositorio oficial:** https://github.com/juandiegos-dev/delivery-app

**Nota:** Las funcionalidades descritas corresponden al alcance y organización del proyecto. Su implementación y estado de avance se verifican mediante el código, las pruebas y las evidencias de cada hito.
