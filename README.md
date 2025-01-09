# La Hora Dulce
![la-hora-dulce-titulo](https://github.com/user-attachments/assets/2430b777-3db1-44c3-ab01-0f2b875507f8)

![version](https://img.shields.io/badge/version-1.0.0-blue.svg) [![GitHub issues open](https://img.shields.io/github/issues/yourusername/la-hora-dulce.svg?maxAge=2592000)](https://github.com/yourusername/la-hora-dulce/issues?q=is%3Aopen+is%3Aissue) [![GitHub issues closed](https://img.shields.io/github/issues-closed-raw/yourusername/la-hora-dulce.svg?maxAge=2592000)](https://github.com/yourusername/la-hora-dulce/issues?q=is%3Aissue+is%3Aclosed)

**La Hora Dulce** es una aplicación diseñada para ayudar a los usuarios a encontrar y compartir recetas deliciosas de postres y desayunos. Proporciona recomendaciones personalizadas, búsquedas avanzadas y una interfaz amigable para explorar la mejor selección de recetas dulces.

---

## Características

- **Recomendaciones Personalizadas:** Descubre recetas adaptadas a tus preferencias.
- **Búsqueda Avanzada:** Encuentra recetas según ingredientes, tus cocineros favoritos, dificultad, y más.
- **Interfaz Intuitiva:** Navegación sencilla y diseño atractivo.
- **Autenticación Segura:** Registro y gestión de cuentas con validación de formularios.
- **Favoritos:** Guarda tus recetas favoritas para acceder a ellas rápidamente.
- **Despliegue Fácil:** Scripts para Docker y Gunicorn/Nginx.

![La Hora Dulce - Vista previa](https://ruta-a-la-imagen-de-ejemplo.com/vista-previa.png)

---

## Tabla de Contenidos

- [Inicio Rápido](#inicio-rápido)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Recursos](#recursos)
- [Licencia](#licencia)

---

## Inicio Rápido

Clona el repositorio e inicia la aplicación localmente:

```bash
# Clona el repositorio
$ git clone https://github.com/yourusername/la-hora-dulce.git
$ cd la-hora-dulce

# Crea un entorno virtual
$ python3 -m venv env
$ source env/bin/activate  # Unix
# .\env\Scripts\activate  # Windows

# Instala las dependencias
$ pip install -r requirements.txt

# Realiza las migraciones
$ python manage.py makemigrations
$ python manage.py migrate

# Inicia el servidor
$ python manage.py runserver
```

Visita `http://127.0.0.1:8000/` en tu navegador para acceder a la aplicación.

---

## Estructura del Proyecto

```bash
< RAÍZ DEL PROYECTO >
   |
   |-- core/                             # Configuraciones principales
   |    |-- settings.py                  # Configuración global
   |    |-- urls.py                      # Rutas principales
   |
   |-- apps/
   |    |-- authentication/              # Lógica de usuarios
   |    |    |-- views.py                
   |    |    |-- urls.py                 
   |    |-- home/                        # Lógica principal de la aplicación
   |    |    |-- views.py                
   |    |    |-- forms.py
   |    |-- scraper/                     # Lógica del scrapping
   |         |-- utils.py                # Obtención de datos
   |         |-- whoosh_index.py         # Definición del esquema y operaciones        
   |
   |-- static/                           # Archivos estáticos
   |    |-- css/, js/, images/           # Recursos estáticos
   |
   |-- templates/                        # Plantillas HTML
        |-- includes/                    # Componentes HTML reutilizables
        |-- layouts/                     # Diseños base
        |-- recetas/                     # Páginas relacionadas con recetas
        |-- usuarios/                    # Páginas de autenticación
```

---

## Creditos

El diseño del frontend de esta aplicación se basa en la plantilla [Argon Dashboard Django](https://www.creative-tim.com/product/argon-dashboard-django) desarrollada por [Creative Tim](https://www.creative-tim.com/) y [AppSeed](https://appseed.us/).

---

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](https://opensource.org/licenses/MIT).

