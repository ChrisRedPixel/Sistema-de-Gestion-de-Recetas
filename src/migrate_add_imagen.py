"""
Migration script to add the 'imagen' column to the recetas table.
This script updates existing databases that were created before the imagen field was added.
"""
import sqlite3
import os

def get_db():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'recetas.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def migrate():
    conn = get_db()
    cursor = conn.cursor()

    # Verificar si la columna ya existe
    cursor.execute("PRAGMA table_info(recetas)")
    columns = [row['name'] for row in cursor.fetchall()]

    if 'imagen' in columns:
        print("La columna 'imagen' ya existe. No se necesita migración.")
        conn.close()
        return

    print("Añadiendo columna 'imagen' a la tabla 'recetas'...")

    # Añadir la columna con un valor por defecto
    cursor.execute("""
        ALTER TABLE recetas ADD COLUMN imagen TEXT NOT NULL DEFAULT 'placeholder_receta.png'
    """)

    conn.commit()
    conn.close()

    print("Migración completada exitosamente!")
    print("Se ha añadido la columna 'imagen' con el valor 'placeholder_receta.png' para las recetas existentes.")

if __name__ == "__main__":
    migrate()
