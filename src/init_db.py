import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'recetas.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def reset_database():
    """Elimina la base de datos actual para permitir una inicialización limpia."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Base de datos eliminada: {DB_PATH}")
    else:
        print(f"La base de datos no existe: {DB_PATH}")

def crear_tablas():
    conn = get_db()
    cursor = conn.cursor()

    # Tabla de usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_usuario TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Tabla de categorías
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL
    )
    """)

    # Tabla de recetas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recetas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descripcion TEXT,
        ingredientes TEXT,
        pasos TEXT,
        tiempo INTEGER,
        porciones INTEGER,
        imagen TEXT NOT NULL,
        id_categoria INTEGER,
        id_usuario INTEGER,
        FOREIGN KEY (id_categoria) REFERENCES categorias(id),
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
    )
    """)

    # Tabla de likes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS likes (
        usuario_id INTEGER,
        receta_id INTEGER,
        PRIMARY KEY (usuario_id, receta_id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY (receta_id) REFERENCES recetas(id)
    )
    """)

    # Tabla de favoritos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS favoritos (
        usuario_id INTEGER,
        receta_id INTEGER,
        PRIMARY KEY (usuario_id, receta_id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY (receta_id) REFERENCES recetas(id)
    )
    """)

    conn.commit()
    conn.close()
    print("Tablas creadas correctamente!")

def inicializar_datos():
    conn = get_db()
    cursor = conn.cursor()

    # Crear usuario admin
    try:
        password_hash = generate_password_hash("admin123")
        cursor.execute(
            "INSERT INTO usuarios (nombre_usuario, email, password) VALUES (?, ?, ?)",
            ("Admin", "admin@recetas.com", password_hash)
        )
        print("Usuario admin creado!")
    except sqlite3.IntegrityError:
        print("Usuario admin ya existe!")

    # Crear categorías en orden
    categorias = [
        "Vegetariano",
        "Keto",
        "Postre",
        "Desayuno",
        "Cenas",
        "Saludable"
    ]

    for cat in categorias:
        try:
            cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (cat,))
            print(f"Categoría '{cat}' creada!")
        except sqlite3.IntegrityError:
            print(f"Categoría '{cat}' ya existe!")

    conn.commit()

    # Obtener ID del usuario admin
    cursor.execute("SELECT id FROM usuarios WHERE email = ?", ("admin@recetas.com",))
    admin_id = cursor.fetchone()[0]

    # Obtener IDs de categorías
    cursor.execute("SELECT id, nombre FROM categorias")
    cats = {row['nombre']: row['id'] for row in cursor.fetchall()}

    # Recetas Vegetarianas
    placeholder_imagen = "placeholder_receta.png"
    recetas_vegetarianas = [
        {
            "titulo": "Ensalada de Quinoa con Vegetales",
            "descripcion": "Una fresca y nutritiva ensalada con quinoa, vegetales crudos y aderezo de limón.",
            "ingredientes": "1 taza de quinoa, 1 pepino, 2 tomates, 1 zanahoria, jugo de limón, aceite de oliva, sal",
            "pasos": "1. Cocinar la quinoa según instrucciones. 2. Picar los vegetales en cubos pequeños. 3. Mezclar todo en un bowl. 4. Aliñar con limón, aceite y sal.",
            "tiempo": 25,
            "porciones": 4
        },
        {
            "titulo": "Lentejas Guisadas con Verduras",
            "descripcion": "Plato caliente y reconfortante de lentejas cocidas con verduras de temporada.",
            "ingredientes": "2 tazas de lentejas, 2 zanahorias, 1 cebolla, 2 papas, 2 dientes de ajo, caldo de verduras",
            "pasos": "1. Remojar lentejas 1 hora. 2. Sofreír cebolla y ajo. 3. Agregar lentejas y verduras picadas. 4. Cubrir con caldo y cocinar 40 min.",
            "tiempo": 60,
            "porciones": 6
        },
        {
            "titulo": "Tacos de Coliflor",
            "descripcion": "Deliciosos tacos vegetarianos con coliflor asado y especias mexicanas.",
            "ingredientes": "1 coliflor grande, tortillas de maíz, 1 cebolla morada, cilantro, limón, comino, pimentón",
            "pasos": "1. Cortar coliflor en floretes. 2. Asar con especias 20 min. 3. Calentar tortillas. 4. Armar tacos con coliflor, cebolla y cilantro.",
            "tiempo": 30,
            "porciones": 4
        }
    ]

    for receta in recetas_vegetarianas:
        try:
            cursor.execute("""
                INSERT INTO recetas (titulo, descripcion, ingredientes, pasos, tiempo, porciones, id_usuario, id_categoria, imagen)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (receta["titulo"], receta["descripcion"], receta["ingredientes"], receta["pasos"],
                  receta["tiempo"], receta["porciones"], admin_id, cats["Vegetariano"], placeholder_imagen))
            print(f"Receta vegetariana '{receta['titulo']}' creada!")
        except sqlite3.IntegrityError:
            print(f"Receta '{receta['titulo']}' ya existe!")

    # Recetas Keto
    recetas_keto = [
        {
            "titulo": "Pollo al Horno con Brócoli y Queso",
            "descripcion": "Plato keto perfecto con pollo jugoso y brócoli cubierto de queso cheddar.",
            "ingredientes": "4 pechugas de pollo, 1 brócoli grande, 1 taza queso cheddar, 2 cdas mantequilla, ajo en polvo",
            "pasos": "1. Sazonar pollo. 2. Hornear 25 min a 180°C. 3. Cocinar brócoli al vapor. 4. Cubrir con queso y gratinar.",
            "tiempo": 35,
            "porciones": 4
        },
        {
            "titulo": "Huevos Revueltos con Aguacate",
            "descripcion": "Desayuno keto rápido y saciante con huevos cremosos y aguacate fresco.",
            "ingredientes": "4 huevos, 1 aguacate, 2 cdas crema, sal, pimienta, cebollín picado",
            "pasos": "1. Batir huevos con crema. 2. Cocinar a fuego bajo. 3. Servir con aguacate en rodajas y cebollín.",
            "tiempo": 10,
            "porciones": 2
        },
        {
            "titulo": "Salmón con Espárragos",
            "descripcion": "Filete de salmón a la plancha acompañado de espárragos salteados.",
            "ingredientes": "2 filetes de salmón, 1 manojo espárragos, 2 cdas aceite de oliva, limón, sal marina",
            "pasos": "1. Sazonar salmón. 2. Cocinar 4 min por lado. 3. Saltear espárragos 5 min. 4. Servir con limón.",
            "tiempo": 15,
            "porciones": 2
        }
    ]

    for receta in recetas_keto:
        try:
            cursor.execute("""
                INSERT INTO recetas (titulo, descripcion, ingredientes, pasos, tiempo, porciones, id_usuario, id_categoria, imagen)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (receta["titulo"], receta["descripcion"], receta["ingredientes"], receta["pasos"],
                  receta["tiempo"], receta["porciones"], admin_id, cats["Keto"], placeholder_imagen))
            print(f"Receta keto '{receta['titulo']}' creada!")
        except sqlite3.IntegrityError:
            print(f"Receta '{receta['titulo']}' ya existe!")

    # Recetas de Postre
    recetas_postre = [
        {
            "titulo": "Brownie de Chocolate Sin Harina",
            "descripcion": "Postre indulgente de chocolate intenso, húmedo y sin harina tradicional.",
            "ingredientes": "200g chocolate amargo, 3 huevos, 1/2 taza azúcar, 100g mantequilla, cacao en polvo",
            "pasos": "1. Derretir chocolate con mantequilla. 2. Batir huevos con azúcar. 3. Mezclar todo. 4. Hornear 25 min a 170°C.",
            "tiempo": 35,
            "porciones": 8
        },
        {
            "titulo": "Mousse de Fresa",
            "descripcion": "Postre ligero y aireado con el sabor dulce de las fresas frescas.",
            "ingredientes": "500g fresas, 1 taza crema para batir, 1/2 taza azúcar, 1 cdta vainilla",
            "pasos": "1. Licuar fresas. 2. Batir crema a punto de chantilly. 3. Mezclar con fresas. 4. Refrigerar 2 horas.",
            "tiempo": 20,
            "porciones": 6
        },
        {
            "titulo": "Cheesecake de Maracuyá",
            "descripcion": "Postre cremoso con base crujiente y topping tropical de maracuyá.",
            "ingredientes": "200g galletas, 500g queso crema, 1 lata leche condensada, 3 maracuyás, 100g mantequilla",
            "pasos": "1. Triturar galletas con mantequilla. 2. Batir queso con leche. 3. Hornear 40 min. 4. Cubrir con pulpa de maracuyá.",
            "tiempo": 60,
            "porciones": 10
        }
    ]

    for receta in recetas_postre:
        try:
            cursor.execute("""
                INSERT INTO recetas (titulo, descripcion, ingredientes, pasos, tiempo, porciones, id_usuario, id_categoria, imagen)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (receta["titulo"], receta["descripcion"], receta["ingredientes"], receta["pasos"],
                  receta["tiempo"], receta["porciones"], admin_id, cats["Postre"], placeholder_imagen))
            print(f"Receta de postre '{receta['titulo']}' creada!")
        except sqlite3.IntegrityError:
            print(f"Receta '{receta['titulo']}' ya existe!")

    # Recetas de Desayuno
    recetas_desayuno = [
        {
            "titulo": "Panqueques de Avena y Banana",
            "descripcion": "Panqueques saludables y esponjosos, perfectos para empezar el día con energía.",
            "ingredientes": "1 taza avena, 2 bananas maduras, 2 huevos, 1 cdta polvo de hornear, canela",
            "pasos": "1. Licuar todos los ingredientes. 2. Calentar sartén. 3. Verter porciones. 4. Cocinar 2 min por lado.",
            "tiempo": 15,
            "porciones": 4
        },
        {
            "titulo": "Tostadas Francesas",
            "descripcion": "Clásico desayuno dulce con pan remojado en leche y huevo, dorado y crujiente.",
            "ingredientes": "4 rebanadas pan, 2 huevos, 1/2 taza leche, 1 cda azúcar, vainilla, canela",
            "pasos": "1. Batir huevos con leche y vainilla. 2. Remojar pan. 3. Dorar en sartén. 4. Servir con miel o fruta.",
            "tiempo": 12,
            "porciones": 2
        },
        {
            "titulo": "Bowl de Yogurt con Granola",
            "descripcion": "Desayuno fresco y crocante con yogurt, granola casera y frutas de temporada.",
            "ingredientes": "2 tazas yogurt griego, 1 taza granola, 1 taza frutos rojos, miel, semillas de chía",
            "pasos": "1. Colocar yogurt en bowls. 2. Agregar granola. 3. Decorar con frutas. 4. Rociar con miel y chía.",
            "tiempo": 5,
            "porciones": 2
        }
    ]

    for receta in recetas_desayuno:
        try:
            cursor.execute("""
                INSERT INTO recetas (titulo, descripcion, ingredientes, pasos, tiempo, porciones, id_usuario, id_categoria, imagen)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (receta["titulo"], receta["descripcion"], receta["ingredientes"], receta["pasos"],
                  receta["tiempo"], receta["porciones"], admin_id, cats["Desayuno"], placeholder_imagen))
            print(f"Receta de desayuno '{receta['titulo']}' creada!")
        except sqlite3.IntegrityError:
            print(f"Receta '{receta['titulo']}' ya existe!")

    # Recetas de Cenas
    recetas_cenas = [
        {
            "titulo": "Sopa de Verduras Nocturna",
            "descripcion": "Sopa ligera y digestiva, ideal para cenar sin sentir pesadez.",
            "ingredientes": "1 calabacín, 1 zanahoria, 1 papa pequeña, 1 cebolla, caldo de pollo, hierbas",
            "pasos": "1. Picar todas las verduras. 2. Hervir en caldo 20 min. 3. Sazonar con hierbas. 4. Servir caliente.",
            "tiempo": 25,
            "porciones": 4
        },
        {
            "titulo": "Omelette de Espinacas",
            "descripcion": "Omelette suave relleno de espinacas salteadas y un toque de queso.",
            "ingredientes": "3 huevos, 2 tazas espinacas, 1/4 taza queso feta, 1 cda aceite, sal",
            "pasos": "1. Saltear espinacas. 2. Batir huevos. 3. Cocinar omelette. 4. Rellenar y doblar.",
            "tiempo": 10,
            "porciones": 1
        },
        {
            "titulo": "Pescado al Vapor con Vegetales",
            "descripcion": "Cena saludable con pescado blanco cocido al vapor junto a vegetales frescos.",
            "ingredientes": "2 filetes de merluza, 1 zanahoria, 1 calabacín, brócoli, limón, eneldo",
            "pasos": "1. Cortar vegetales. 2. Colocar en vaporera con pescado. 3. Cocinar 15 min. 4. Servir con limón y eneldo.",
            "tiempo": 20,
            "porciones": 2
        }
    ]

    for receta in recetas_cenas:
        try:
            cursor.execute("""
                INSERT INTO recetas (titulo, descripcion, ingredientes, pasos, tiempo, porciones, id_usuario, id_categoria, imagen)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (receta["titulo"], receta["descripcion"], receta["ingredientes"], receta["pasos"],
                  receta["tiempo"], receta["porciones"], admin_id, cats["Cenas"], placeholder_imagen))
            print(f"Receta de cena '{receta['titulo']}' creada!")
        except sqlite3.IntegrityError:
            print(f"Receta '{receta['titulo']}' ya existe!")

    # Recetas Saludables
    recetas_saludables = [
        {
            "titulo": "Bowl de Buddha",
            "descripcion": "Bowl nutritivo y balanceado con granos, vegetales y proteína vegetal.",
            "ingredientes": "1/2 taza quinoa, 1/2 taza garbanzos, 1 zanahoria, 1/2 aguacate, espinacas, tahini",
            "pasos": "1. Cocinar quinoa y garbanzos. 2. Armar bowl con vegetales. 3. Aliñar con tahini y limón.",
            "tiempo": 20,
            "porciones": 1
        },
        {
            "titulo": "Wrap de Lechuga con Pollo",
            "descripcion": "Alternativa low-carb a los wraps tradicionales, usando hojas de lechuga.",
            "ingredientes": "4 hojas lechuga romana, 1 pechuga pollo, 1 zanahoria, 1 pepino, hummus",
            "pasos": "1. Cocinar y desmenuzar pollo. 2. Cortar vegetales en juliana. 3. Rellenar hojas de lechuga. 4. Enrollar y servir.",
            "tiempo": 15,
            "porciones": 2
        },
        {
            "titulo": "Smoothie Verde Detox",
            "descripcion": "Bebida energizante con vegetales de hoja verde y frutas para depurar el organismo.",
            "ingredientes": "1 taza espinacas, 1/2 pepino, 1 manzana verde, jugo de 1 limón, 1 vaso agua",
            "pasos": "1. Lavar todos los ingredientes. 2. Cortar en trozos. 3. Licuar hasta obtener mezcla homogénea. 4. Servir frío.",
            "tiempo": 5,
            "porciones": 1
        }
    ]

    for receta in recetas_saludables:
        try:
            cursor.execute("""
                INSERT INTO recetas (titulo, descripcion, ingredientes, pasos, tiempo, porciones, id_usuario, id_categoria, imagen)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (receta["titulo"], receta["descripcion"], receta["ingredientes"], receta["pasos"],
                  receta["tiempo"], receta["porciones"], admin_id, cats["Saludable"], placeholder_imagen))
            print(f"Receta saludable '{receta['titulo']}' creada!")
        except sqlite3.IntegrityError:
            print(f"Receta '{receta['titulo']}' ya existe!")

    conn.commit()
    conn.close()
    print("\n¡Base de datos inicializada exitosamente!")
    print("\nCredenciales de admin:")
    print("  Email: admin@recetas.com")
    print("  Password: admin123")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_database()
    crear_tablas()
    inicializar_datos()
