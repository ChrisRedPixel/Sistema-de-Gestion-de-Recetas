import sqlite3
from db import *
# Connect to the database
conn = sqlite3.connect("recetas.db")
c = conn.cursor()

# # Create tables
# c.execute("""
# CREATE TABLE IF NOT EXISTS usuarios (
#     id INTEGER PRIMARY KEY, 
#     nombre TEXT UNIQUE
# )
# """)
# c.execute("""
# CREATE TABLE IF NOT EXISTS recetas (
#     id INTEGER PRIMARY KEY, 
#     nombre TEXT
# )
# """)
# c.execute("""
# CREATE TABLE IF NOT EXISTS likes (
#     usuario_id INTEGER, 
#     receta_id INTEGER, 
#     UNIQUE(usuario_id, receta_id)
# )
# """)

# Add a new user
# def add_user(n):
#     try:
#         c.execute("INSERT INTO usuarios(nombre) VALUES(?)", (n,))
#         conn.commit()
#     except sqlite3.IntegrityError:
#         print("Usuario ya existe")

# # Add a new recipe
# def add_receta(r):
#     c.execute("INSERT INTO recetas(nombre) VALUES(?)", (r,))
#     conn.commit()

# Like a recipe
def like(u, r):
    c.execute("SELECT id FROM usuarios WHERE nombre=?", (u,))
    x = c.fetchone()
    if x:
        try:
            c.execute("INSERT INTO likes(usuario_id, receta_id) VALUES(?, ?)", (x[0], r))
            conn.commit()
        except sqlite3.IntegrityError:
            print("Ya se dio like a esta receta")
    else:
        print("Usuario no encontrado")

# Unlike a recipe
def unlike(u, r):
    c.execute("SELECT id FROM usuarios WHERE nombre=?", (u,))
    x = c.fetchone()
    if x:
        c.execute("DELETE FROM likes WHERE usuario_id=? AND receta_id=?", (x[0], r))
        conn.commit()
    else:
        print("Usuario no encontrado")

# Count likes for a recipe
def count(r):
    c.execute("SELECT COUNT(*) FROM likes WHERE receta_id=?", (r,))
    print("Likes:", c.fetchone()[0])

# Test the functionality
# add_user("Bernie")
# add_receta("Arroz")
# like("Bernie", 1)
# count(1)
# unlike("Bernie", 1)
# count(1)

# Close the connection
conn.close()