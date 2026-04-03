from db import get_db
import sqlite3

def registrar_usuario(nombre_usuario, email, password):
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO usuarios (nombre_usuario, email, password)
        VALUES (?, ?, ?)
        """, (nombre_usuario, email, password))
        conn.commit()
        print("Usuario registrado!")
    except sqlite3.IntegrityError:
        print("Error: el email ya existe!")
    finally:
        conn.close()