import sqlite3
from db import *
# Conexión a la base de datos
conexion = sqlite3.connect("recetas.db")
cursor = conexion.cursor()

# # Crear tabla
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS recetas (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     nombre TEXT
# )
# """)
# conexion.commit()

# Función añadir
def anadir(nombre):
    cursor.execute("INSERT INTO recetas (nombre) VALUES (?)", (nombre,))
    conexion.commit()
    print(f"{nombre} se añadió a tus favoritos")

# Función quitar
def quitar(nombre):
    cursor.execute("DELETE FROM recetas WHERE nombre = ?", (nombre,))
    conexion.commit()
    print(f"{nombre} se quitó de tus favoritos")

# Menú (2 opciones)
while True:
    print("\n1. Añadir receta")
    print("2. Quitar receta")

    op = input("Opción: ")

    if op == "1":
        nombre = input("flan de coco: ")
        anadir(nombre)

    elif op == "2":
        nombre = input("Arroz Griego: ")
        quitar(nombre)

    else:
        print("Opción inválida")