from db import get_db

def ver_usuarios():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    for u in usuarios:
        print(u)

    conn.close()