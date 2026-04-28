import sqlite3

conn = sqlite3.connect("recetas.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM usuarios")
usuarios = cursor.fetchall()

for u in usuarios:
    print(u)

conn.close()