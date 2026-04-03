import sqlite3

# CONEXIÓN A LA BASE DE DATOS xd
def get_db():
    return sqlite3.connect("recetas.db")


# CREAR TABLA CATEGORIAS
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


# CREAR TABLA RECETAS
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
        id_categoria INTEGER,
        FOREIGN KEY (id_categoria) REFERENCES categorias(id)
    )
    """)

    conn.commit()
    conn.close()


# REGISTRAR CATEGORIA
def registrar_categoria(nombre):
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre,))
        conn.commit()
        print(f"Categoría '{nombre}' creada!")
    except sqlite3.IntegrityError:
        print(" Esa categoría ya existe.")
    finally:
        conn.close()


# VER CATEGORIAS
def ver_categorias():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()

    print("\n Categorías disponibles:")
    for c in categorias:
        print(f"{c[0]} - {c[1]}")

    conn.close()


# REGISTRAR RECETA
def registrar_receta():
    conn = get_db()
    cursor = conn.cursor()

    print("\n=== REGISTRAR RECETA ===")

    titulo = input("Título: ")
    descripcion = input("Descripción: ")
    ingredientes = input("Ingredientes: ")
    pasos = input("Pasos: ")

    try:
        tiempo = int(input("Tiempo (minutos): "))
        porciones = int(input("Porciones: "))
    except ValueError:
        print(" Error: tiempo y porciones deben ser números.")
        conn.close()
        return

    # Mostrar categorías antes de elegir
    ver_categorias()
    try:
        id_categoria = int(input("Selecciona el ID de la categoría: "))
    except ValueError:
        print(" ID inválido.")
        conn.close()
        return

    cursor.execute("""
    INSERT INTO recetas (titulo, descripcion, ingredientes, pasos, tiempo, porciones, id_categoria)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (titulo, descripcion, ingredientes, pasos, tiempo, porciones, id_categoria))

    conn.commit()
    conn.close()

    print("Receta registrada correctamente!")


# MAIN
if __name__ == "__main__":
    crear_tabla_categorias()
    crear_tabla_recetas()

    registrar_categoria("Vegetariano")
    registrar_categoria("Keto")
    registrar_categoria("Postres")

    registrar_receta()