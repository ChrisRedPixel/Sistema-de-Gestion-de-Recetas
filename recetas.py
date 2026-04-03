from db import get_db
from categorias import ver_categorias

def registrar_receta(id_usuario):
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
        print("Error: valores inválidos.")
        conn.close()
        return

    ver_categorias()

    try:
        id_categoria = int(input("Selecciona ID categoría: "))
    except ValueError:
        print("ID inválido.")
        conn.close()
        return

    cursor.execute("""
    INSERT INTO recetas (titulo, descripcion, ingredientes, pasos, tiempo, porciones, id_categoria, id_usuario)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (titulo, descripcion, ingredientes, pasos, tiempo, porciones, id_categoria, id_usuario))

    conn.commit()
    conn.close()

    print("Receta registrada!")