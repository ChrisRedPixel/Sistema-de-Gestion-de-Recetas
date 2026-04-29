"""
Plantilla para migraciones de la base de datos.

Uso: python migrate_template.py

Este script es idempotente - puede ejecutarse múltiples veces sin causar errores.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'recetas.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def migrate():
    """
    Agregar aquí los cambios de schema.

    Ejemplos de operaciones:
    - ALTER TABLE tabla ADD COLUMN columna tipo
    - CREATE TABLE nueva_tabla (...)
    - CREATE INDEX IF NOT EXISTS idx_nombre ON tabla(columna)
    """
    conn = get_db()
    cursor = conn.cursor()

    # --- TU CÓDIGO DE MIGRACIÓN AQUÍ ---
    # Ejemplo:
    # cursor.execute("ALTER TABLE recetas ADD COLUMN dificultad TEXT DEFAULT 'media'")
    # -----------------------------------

    conn.commit()
    conn.close()
    print("Migración completada exitosamente!")

if __name__ == "__main__":
    migrate()
