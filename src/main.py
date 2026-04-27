import sqlite3
from registro_recetasCRUD import (
    get_db, crear_tabla_usuarios, crear_tabla_categorias, crear_tabla_recetas,
    registrar_usuario, listar_usuarios, actualizar_usuario, eliminar_usuario,
    registrar_categoria, listar_categorias, actualizar_categoria, eliminar_categoria,
    registrar_receta, listar_recetas, actualizar_receta, eliminar_receta,
    listar_recetas_por_usuario, listar_recetas_por_categoria, buscar_recetas
)

# =======================
# SISTEMA DE LOGIN
# =======================
def login():
    """Sistema de login - NO muestra barra de búsqueda"""
    print("\n" + "="*50)
    print("       SISTEMA DE GESTION DE RECETAS")
    print("="*50)

    while True:
        print("\n--- INICIO DE SESION ---")
        email = input("Email: ")
        password = input("Password: ")

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM usuarios WHERE email=? AND password=?", (email, password))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            print(f"\nBienvenido, {usuario[1]}!")
            return {"id": usuario[0], "nombre": usuario[1]}
        else:
            print("Credenciales incorrectas!")
            print("1. Intentar de nuevo")
            print("2. Registrarse como nuevo usuario")
            print("3. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "2":
                nombre = input("Nombre: ")
                email = input("Email: ")
                password = input("Password: ")
                registrar_usuario(nombre, email, password)
            elif opcion == "3":
                return None

def logout():
    """Muestra mensaje de logout - NO muestra barra de búsqueda"""
    print("\n" + "="*50)
    print("       SESION CERRADA - HASTA PRONTO!")
    print("="*50 + "\n")

# =======================
# BARRA DE BUSQUEDA
# =======================
def mostrar_barra_busqueda():
    """Muestra la barra de búsqueda y permite buscar recetas"""
    print("\n" + "-"*40)
    print("🔍 BARRA DE BUSQUEDA DE RECETAS")
    print("-"*40)
    busqueda = input("Ingrese término de búsqueda (título, ingrediente, descripción): ")

    if busqueda.strip():
        resultados = buscar_recetas(busqueda)
        if resultados:
            print(f"\n✅ Se encontraron {len(resultados)} receta(s):")
            for r in resultados:
                print(f"\n  ID: {r[0]}")
                print(f"  Título: {r[1]}")
                print(f"  Descripción: {r[2]}")
                print(f"  Ingredientes: {r[3]}")
                print(f"  Tiempo: {r[4]} min | Porciones: {r[5]}")
                print(f"  Usuario: {r[6]} | Categoría: {r[7]}")
        else:
            print("\n❌ No se encontraron recetas con ese término.")
    else:
        print("Búsqueda vacía.")
    print("-"*40)

# =======================
# MENUS PRINCIPALES (CON BUSQUEDA)
# =======================
def menu_principal(usuario):
    """Menú principal - CON barra de búsqueda"""
    while True:
        print("\n" + "="*50)
        print(f"       MENU PRINCIPAL - {usuario['nombre'].upper()}")
        print("="*50)
        print("1. Gestionar Recetas")
        print("2. Gestionar Categorias")
        print("3. Gestionar Usuarios")
        print("4. 🔍 Buscar Recetas")
        print("5. Cerrar Sesión")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            menu_recetas(usuario)
        elif opcion == "2":
            menu_categorias()
        elif opcion == "3":
            menu_usuarios()
        elif opcion == "4":
            mostrar_barra_busqueda()
        elif opcion == "5":
            logout()
            break
        else:
            print("Opción inválida!")

def menu_recetas(usuario):
    """Menú de recetas - CON barra de búsqueda"""
    while True:
        print("\n" + "-"*40)
        print("       GESTION DE RECETAS")
        print("-"*40)
        print("1. Listar todas las recetas")
        print("2. Registrar nueva receta")
        print("3. Actualizar receta")
        print("4. Eliminar receta")
        print("5. Ver recetas por usuario")
        print("6. Ver recetas por categoría")
        print("7. 🔍 Buscar recetas")
        print("8. Volver al menú principal")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            recetas = listar_recetas()
            if recetas:
                for r in recetas:
                    print(f"\n  [{r[0]}] {r[1]} - {r[2]}")
                    print(f"      Ingredientes: {r[3]}")
                    print(f"      Usuario: {r[7]} | Categoría: {r[8]}")
            else:
                print("No hay recetas registradas.")
        elif opcion == "2":
            titulo = input("Título: ")
            descripcion = input("Descripción: ")
            ingredientes = input("Ingredientes: ")
            pasos = input("Pasos: ")
            tiempo = int(input("Tiempo (min): "))
            porciones = int(input("Porciones: "))
            print("Categorías disponibles:")
            categorias = listar_categorias()
            for c in categorias:
                print(f"  {c[0]}. {c[1]}")
            id_categoria = int(input("ID de categoría: "))

            registrar_receta(titulo, descripcion, ingredientes, pasos, tiempo,
                           porciones, usuario["id"], id_categoria)
        elif opcion == "3":
            id_receta = int(input("ID de receta a actualizar: "))
            print("Deje en blanco si no desea actualizar un campo")
            titulo = input("Nuevo título: ") or None
            descripcion = input("Nueva descripción: ") or None
            ingredientes = input("Nuevos ingredientes: ") or None
            pasos = input("Nuevos pasos: ") or None
            tiempo_str = input("Nuevo tiempo: ")
            tiempo = int(tiempo_str) if tiempo_str else None
            porciones_str = input("Nuevas porciones: ")
            porciones = int(porciones_str) if porciones_str else None
            cat_str = input("Nueva ID de categoría: ")
            id_categoria = int(cat_str) if cat_str else None

            actualizar_receta(id_receta, titulo, descripcion, ingredientes,
                            pasos, tiempo, porciones, id_categoria)
        elif opcion == "4":
            id_receta = int(input("ID de receta a eliminar: "))
            eliminar_receta(id_receta)
        elif opcion == "5":
            id_usuario = int(input("ID de usuario: "))
            recetas = listar_recetas_por_usuario(id_usuario)
            for r in recetas:
                print(f"\n  [{r[0]}] {r[1]} - {r[2]}")
        elif opcion == "6":
            id_categoria = int(input("ID de categoría: "))
            recetas = listar_recetas_por_categoria(id_categoria)
            for r in recetas:
                print(f"\n  [{r[0]}] {r[1]} - {r[2]}")
        elif opcion == "7":
            mostrar_barra_busqueda()
        elif opcion == "8":
            break
        else:
            print("Opción inválida!")

def menu_categorias():
    """Menú de categorías - CON barra de búsqueda"""
    while True:
        print("\n" + "-"*40)
        print("       GESTION DE CATEGORIAS")
        print("-"*40)
        print("1. Listar categorías")
        print("2. Registrar categoría")
        print("3. Actualizar categoría")
        print("4. Eliminar categoría")
        print("5. 🔍 Buscar recetas por categoría")
        print("6. Volver")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            categorias = listar_categorias()
            for c in categorias:
                print(f"  {c[0]}. {c[1]}")
        elif opcion == "2":
            nombre = input("Nombre de la categoría: ")
            registrar_categoria(nombre)
        elif opcion == "3":
            id_categoria = int(input("ID de categoría: "))
            nombre = input("Nuevo nombre: ")
            actualizar_categoria(id_categoria, nombre)
        elif opcion == "4":
            id_categoria = int(input("ID de categoría a eliminar: "))
            eliminar_categoria(id_categoria)
        elif opcion == "5":
            mostrar_barra_busqueda()
        elif opcion == "6":
            break
        else:
            print("Opción inválida!")

def menu_usuarios():
    """Menú de usuarios - CON barra de búsqueda"""
    while True:
        print("\n" + "-"*40)
        print("       GESTION DE USUARIOS")
        print("-"*40)
        print("1. Listar usuarios")
        print("2. Registrar usuario")
        print("3. Actualizar usuario")
        print("4. Eliminar usuario")
        print("5. 🔍 Buscar recetas")
        print("6. Volver")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            usuarios = listar_usuarios()
            for u in usuarios:
                print(f"  {u[0]}. {u[1]} ({u[2]})")
        elif opcion == "2":
            nombre = input("Nombre: ")
            email = input("Email: ")
            password = input("Password: ")
            registrar_usuario(nombre, email, password)
        elif opcion == "3":
            id_usuario = int(input("ID de usuario: "))
            print("Deje en blanco si no desea actualizar")
            nombre = input("Nuevo nombre: ") or None
            email = input("Nuevo email: ") or None
            password = input("Nueva password: ") or None
            actualizar_usuario(id_usuario, nombre, email, password)
        elif opcion == "4":
            id_usuario = int(input("ID de usuario a eliminar: "))
            eliminar_usuario(id_usuario)
        elif opcion == "5":
            mostrar_barra_busqueda()
        elif opcion == "6":
            break
        else:
            print("Opción inválida!")

# =======================
# PROGRAMA PRINCIPAL
# =======================
if __name__ == "__main__":
    # Crear tablas si no existen
    crear_tabla_usuarios()
    crear_tabla_categorias()
    crear_tabla_recetas()

    # Iniciar sesión
    usuario = login()

    if usuario:
        # Menú principal (CON búsqueda)
        menu_principal(usuario)
    else:
        print("\nGracias por usar el Sistema de Gestión de Recetas!")
