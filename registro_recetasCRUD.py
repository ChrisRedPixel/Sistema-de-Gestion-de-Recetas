import sqlite3

# Función para conectarse a la base de datos
def get_db():
    return sqlite3.connect("recetas.db")

# =======================
# CREACIÓN DE TABLAS
# =======================
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

# =======================
# CRUD USUARIOS
# =======================
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

def listar_usuarios():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def actualizar_usuario(id_usuario, nombre=None, email=None, password=None):
    conn = get_db()
    cursor = conn.cursor()
    if nombre:
        cursor.execute("UPDATE usuarios SET nombre=? WHERE id=?", (nombre, id_usuario))
    if email:
        cursor.execute("UPDATE usuarios SET email=? WHERE id=?", (email, id_usuario))
    if password:
        cursor.execute("UPDATE usuarios SET password=? WHERE id=?", (password, id_usuario))
    conn.commit()
    conn.close()
    print(f"Usuario {id_usuario} actualizado!")

def eliminar_usuario(id_usuario):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id=?", (id_usuario,))
    conn.commit()
    conn.close()
    print(f"Usuario {id_usuario} eliminado!")

# =======================
# CRUD CATEGORIAS
# =======================
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

def listar_categorias():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()
    conn.close()
    return categorias

def actualizar_categoria(id_categoria, nombre):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE categorias SET nombre=? WHERE id=?", (nombre, id_categoria))
    conn.commit()
    conn.close()
    print(f"Categoría {id_categoria} actualizada!")

def eliminar_categoria(id_categoria):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categorias WHERE id=?", (id_categoria,))
    conn.commit()
    conn.close()
    print(f"Categoría {id_categoria} eliminada!")

# =======================
# CRUD RECETAS
# =======================
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

def listar_recetas():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT r.id, r.titulo, r.descripcion, r.ingredientes, r.pasos, r.tiempo, r.porciones,
           u.nombre as usuario, c.nombre as categoria
    FROM recetas r
    JOIN usuarios u ON r.id_usuario = u.id
    LEFT JOIN categorias c ON r.id_categoria = c.id
    """)
    recetas = cursor.fetchall()
    conn.close()
    return recetas

def actualizar_receta(id_receta, titulo=None, descripcion=None, ingredientes=None, pasos=None, tiempo=None, porciones=None, id_categoria=None):
    conn = get_db()
    cursor = conn.cursor()
    if titulo:
        cursor.execute("UPDATE recetas SET titulo=? WHERE id=?", (titulo, id_receta))
    if descripcion:
        cursor.execute("UPDATE recetas SET descripcion=? WHERE id=?", (descripcion, id_receta))
    if ingredientes:
        cursor.execute("UPDATE recetas SET ingredientes=? WHERE id=?", (ingredientes, id_receta))
    if pasos:
        cursor.execute("UPDATE recetas SET pasos=? WHERE id=?", (pasos, id_receta))
    if tiempo:
        cursor.execute("UPDATE recetas SET tiempo=? WHERE id=?", (tiempo, id_receta))
    if porciones:
        cursor.execute("UPDATE recetas SET porciones=? WHERE id=?", (porciones, id_receta))
    if id_categoria:
        cursor.execute("UPDATE recetas SET id_categoria=? WHERE id=?", (id_categoria, id_receta))
    conn.commit()
    conn.close()
    print(f"Receta {id_receta} actualizada!")

def eliminar_receta(id_receta):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recetas WHERE id=?", (id_receta,))
    conn.commit()
    conn.close()
    print(f"Receta {id_receta} eliminada!")

def listar_recetas_por_usuario(id_usuario):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recetas WHERE id_usuario=?", (id_usuario,))
    recetas = cursor.fetchall()
    conn.close()
    return recetas

def listar_recetas_por_categoria(id_categoria):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recetas WHERE id_categoria=?", (id_categoria,))
    recetas = cursor.fetchall()
    conn.close()
    return recetas

# =======================
# EJEMPLO DE USO
# =======================
if __name__ == "__main__":
    crear_tabla_usuarios()
    crear_tabla_categorias()
    crear_tabla_recetas()

    # Registrar un usuario
    registrar_usuario("Alayna", "alayna@example.com", "1234")

    # Registrar categorías
    registrar_categoria("Vegetariano")
    registrar_categoria("Keto")

    # Registrar recetas
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

    # Listar recetas
    recetas = listar_recetas()
    for r in recetas:
        print(r)