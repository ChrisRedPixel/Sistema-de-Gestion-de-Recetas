from db import get_db
import sqlite3

def registrar_categoria(nombre):
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre,))
        conn.commit()
        print(f"Categoría '{nombre}' creada!")
    except sqlite3.IntegrityError:
        print("Esa categoría ya existe.")
    finally:
        conn.close()


def ver_categorias():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()

    print("\nCategorías disponibles:")
    for c in categorias:
        print(f"{c[0]} - {c[1]}")

    conn.close()