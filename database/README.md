# Base de Datos - Instrucciones para el Equipo

## ¿Por qué las bases de datos no se sincronizan con Git?

Los archivos `.db` de SQLite están excluidos en `.gitignore` intencionalmente porque:
- Son archivos binarios que cambian constantemente
- Git no puede hacer merge de cambios en archivos binarios
- Cada desarrollador debe tener su propia copia local

## Inicializar la base de datos (al clonar el repo)

Cada integrante del equipo debe ejecutar esto después de clonar:

```bash
cd src
python init_db.py
```

Esto creará:
- Todas las tablas necesarias
- Usuario admin (email: `admin@recetas.com`, password: `admin123`)
- 6 categorías (Vegetariano, Keto, Postre, Desayunos, Cenas, Saludable)
- 18 recetas de ejemplo

## Resetear la base de datos completamente

Si necesitas limpiar todo y empezar desde cero:

```bash
python init_db.py --reset
python init_db.py
```

## Agregar nuevas migraciones (cambios al schema)

Si necesitas modificar la estructura de la base de datos:

1. Crea un script en `src/` con el formato `migrate_<descripcion>.py`
2. El script debe:
   - Conectarse a `database/recetas.db`
   - Usar `ALTER TABLE` o crear nuevas tablas
   - Ser idempotente (puede ejecutarse múltiples veces sin romper nada)

Ejemplo: `src/migrate_add_imagen.py`

## Estructura actual de la base de datos

### Tablas:
- `usuarios` - Usuarios registrados
- `categorias` - Categorías de recetas
- `recetas` - Recetas con ingredientes, pasos, tiempos
- `likes` - Likes de usuarios a recetas (tabla intermedia)
- `favoritos` - Favoritos de usuarios (tabla intermedia)

### Credenciales por defecto:
```
Email: admin@recetas.com
Password: admin123
```
