import sqlite3

#Función para conectarse a la base de datos
def get_db():
    return sqlite3.connect("recetas.db")

#Función para crear la tabla usuarios si no existe
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

#Función para registrar un usuario
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

#Esto solo se ejecuta si corres este archivo directamente
if __name__ == "__main__":
    crear_tabla_usuarios()

    #Prueba rápida de registro
    nombre = input("Nombre: ")
    email = input("Email: ")
    password = input("Password: ")

    registrar_usuario(nombre, email, password)