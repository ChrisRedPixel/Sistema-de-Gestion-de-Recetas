import sqlite3

# Función para conectarse a la base de datos
def get_db():
    return sqlite3.connect("recetas.db")

# Crear tabla usuarios
def crear_tabla_usuarios():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    print("Tabla usuarios creada!")

# Crear tabla categorías
def crear_tabla_categorias():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    print("Tabla categorias creada!")

# Crear tabla recetas
def crear_tabla_recetas():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recetas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descripcion TEXT,
        ingredientes TEXT,
        pasos TEXT,
        tiempo INTEGER,
        porciones INTEGER,
        id_usuario INTEGER NOT NULL,
        id_categoria INTEGER,
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
        FOREIGN KEY (id_categoria) REFERENCES categorias(id)
    )
    """)

    conn.commit()
    conn.close()
    print("Tabla recetas creada!")

# Función para registrar un usuario
def registrar_usuario(nombre, email, password):
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO usuarios (nombre, email, password)
        VALUES (?, ?, ?)
        """, (nombre, email, password))

        conn.commit()
        print("Usuario registrado!")
    except sqlite3.IntegrityError:
        print("Error: el email ya existe!")
    finally:
        conn.close()

# Función para registrar categoría
def registrar_categoria(nombre):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre,))
        conn.commit()
        print(f"Categoría '{nombre}' creada!")
    except sqlite3.IntegrityError:
        print("La categoría ya existe!")
    finally:
        conn.close()

# Función para registrar receta
def registrar_receta(titulo, descripcion, ingredientes, pasos, tiempo, porciones, id_usuario, id_categoria):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO recetas (titulo, descripcion, ingredientes, pasos, tiempo, porciones, id_usuario, id_categoria)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (titulo, descripcion, ingredientes, pasos, tiempo, porciones, id_usuario, id_categoria))
    conn.commit()
    conn.close()
    print(f"Receta '{titulo}' registrada!")

# Crear todas las tablas
if __name__ == "__main__":
    crear_tabla_usuarios()
    crear_tabla_categorias()
    crear_tabla_recetas()

    # Ejemplo rápido de registro
    nombre = input("Nombre: ")
    email = input("Email: ")
    password = input("Password: ")
    registrar_usuario(nombre, email, password)

    registrar_categoria("Vegetariano")
    registrar_categoria("Keto")

    registrar_receta(
        titulo="Ensalada de Quinoa",
        descripcion="Ensalada fresca con quinoa y vegetales",
        ingredientes="Quinoa, tomate, pepino, zanahoria",
        pasos="1. Cocinar quinoa\n2. Mezclar con vegetales\n3. Aliñar al gusto",
        tiempo=20,
        porciones=2,
        id_usuario=1,
        id_categoria=1
    )