from db import get_db
import sqlite3

def like(usuario_id, receta_id):
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO likes (usuario_id, receta_id)
        VALUES (?, ?)
        """, (usuario_id, receta_id))
        conn.commit()
        print("Like agregado!")
    except sqlite3.IntegrityError:
        print("Ya diste like.")
    finally:
        conn.close()


def unlike(usuario_id, receta_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM likes WHERE usuario_id=? AND receta_id=?
    """, (usuario_id, receta_id))

    conn.commit()
    conn.close()
    print("Like eliminado!")


def contar_likes(receta_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM likes WHERE receta_id=?", (receta_id,))
    print("Likes:", cursor.fetchone()[0])

    conn.close()