# My Cooking - Sistema de Gestión de Recetas

Una aplicación web adaptativa y responsiva para compartir y gestionar recetas de cocina.

## Características

- **Registro de usuarios**: Sistema de autenticación con registro y login seguro
- **Gestión de recetas**: CRUD completo para crear, editar y eliminar recetas
- **Categorías**: Organización de recetas por categorías (Vegetariano, Keto, Postres, etc.)
- **Sistema de likes**: Votar por las recetas de otros usuarios
- **Favoritos**: Guardar recetas favoritas en un inventario personal
- **Perfiles de usuario**: Ver las recetas publicadas por cada usuario
- **Diseño responsivo**: Interfaz adaptativa con Tailwind CSS

## Tecnologías

- **Backend**: Python con Flask
- **Frontend**: HTML5, Tailwind CSS (CDN)
- **Base de datos**: SQLite

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Inicializar la base de datos (desde la raíz del proyecto):
```bash
cd src
python init_db.py
```

3. Ejecutar la aplicación:
```bash
python app.py
```

4. Abrir el navegador en http://127.0.0.1:5000

### Credenciales por defecto
```
Email: admin@recetas.com
Password: admin123
```

## Nota para el equipo de desarrollo

La base de datos (`recetas.db`) es un archivo SQLite local que **no se sincroniza con Git**. Cada desarrollador debe inicializar su propia copia ejecutando `init_db.py` después de clonar o hacer pull de cambios en el schema.

Ver `database/README.md` para más detalles sobre migraciones y reset de la base de datos.

## Estructura del Proyecto

```
├── app.py              # Aplicación principal Flask
├── init_db.py          # Inicialización de la base de datos
├── requirements.txt    # Dependencias de Python
├── templates/          # Plantillas HTML
│   ├── base.html       # Plantilla base
│   ├── index.html      # Página principal
│   ├── login.html      # Inicio de sesión
│   ├── registro.html   # Registro de usuarios
│   ├── receta_form.html # Formulario de recetas
│   ├── receta_detalle.html # Detalle de receta
│   ├── mis_recetas.html # Lista de mis recetas
│   ├── favoritos.html  # Recetas favoritas
│   └── perfil.html     # Perfil de usuario
└── recetas.db          # Base de datos SQLite
```

## Uso

1. **Registrarse**: Crear una cuenta nueva
2. **Explorar recetas**: Ver todas las recetas de la comunidad
3. **Crear receta**: Añadir tus propias recetas con ingredientes y pasos
4. **Votar**: Dar like a las recetas que te gusten
5. **Favoritos**: Guardar recetas para acceder rápidamente
6. **Perfil**: Ver las recetas publicadas por otros usuarios

## Autor

Desarrollado como proyecto de aplicación web adaptativa - Grupo Software3vision
