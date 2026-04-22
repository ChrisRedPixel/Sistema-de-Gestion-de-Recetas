import sqlite3

def get_db():
    conn = sqlite3.connect("database/recetas.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def crear_tablas():
    conn = get_db()
    cursor = conn.cursor()

    # Tabla de usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_usuario TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Tabla de categorías
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL
    )
    """)

    # Tabla de recetas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recetas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descripcion TEXT,
        ingredientes TEXT,
        pasos TEXT,
        tiempo INTEGER,
        porciones INTEGER,
        id_categoria INTEGER,
        id_usuario INTEGER,
        FOREIGN KEY (id_categoria) REFERENCES categorias(id),
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
    )
    """)

    # Tabla de likes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS likes (
        usuario_id INTEGER,
        receta_id INTEGER,
        PRIMARY KEY (usuario_id, receta_id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY (receta_id) REFERENCES recetas(id)
    )
    """)

    # Tabla de favoritos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS favoritos (
        usuario_id INTEGER,
        receta_id INTEGER,
        PRIMARY KEY (usuario_id, receta_id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY (receta_id) REFERENCES recetas(id)
    )
    """)

    conn.commit()

    # Insertar categorías por defecto
    categorias_defecto = ['Vegetariano', 'Keto', 'Postres', 'Desayunos', 'Cenas', 'Saludable']
    for cat in categorias_defecto:
        try:
            cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (cat,))
        except sqlite3.IntegrityError:
            pass  # Ya existe

    conn.commit()
    conn.close()
    print("Tablas creadas correctamente!")

if __name__ == "__main__":
    crear_tablas()
