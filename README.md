# My Cooking - Sistema de Gestión de Recetas

Una aplicación web adaptativa y responsiva para compartir y gestionar recetas de cocina.

## Integrantes 

- Josean C. Jimenez Pagan
- Alayna Vázquez Hernández
- Christian Aleman González
- Bernie Muñiz Rios

##  El Problema

Para muchos entusiastas de la cocina, mantener un registro ordenado de sus recetas suele ser un desafío. La dispersión de notas en papel, enlaces guardados y mensajes de texto suele provocar:
*  **Pérdida de información:** Recetas valiosas que se olvidan o se extravían con el tiempo.
*  **Búsqueda ineficiente:** Dificultad y pérdida de tiempo al intentar localizar un plato específico.
*  **Falta de estructura:** Ausencia de un formato unificado para organizar ingredientes, pasos y categorías.

##  La Solución

Este proyecto nace con el objetivo de resolver este desorden mediante una **plataforma digital centralizada**. El sistema permite almacenar, modificar y consultar cualquier receta de forma intuitiva, optimizando la gestión culinaria y asegurando que tus preparaciones favoritas estén siempre a un solo clic de distancia.

##  Objetivo del sistema

La aplicación ofrece un flujo completo de gestión de contenidos (CRUD) diseñado para optimizar la experiencia del usuario a través de las siguientes funcionalidades:

*  **Gestión y Almacenamiento:** Permite registrar nuevas recetas desde cero, capturando detalladamente los ingredientes necesarios, las porciones y los pasos cronológicos de preparación dentro de una base de datos centralizada.
*  **Mantenimiento de Información:** Automatiza la actualización de recetas existentes para corregir o añadir detalles, así como la eliminación definitiva de aquellos registros que ya no se consideren necesarios.
*  **Consulta Inteligente y Eficiente:** Facilita la exploración, filtrado y visualización ágil del catálogo de recetas guardadas, reduciendo el tiempo de búsqueda mediante una interfaz organizada.

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
