# main.py
from olds_files.usuarios import crear_tabla_usuarios, registrar_usuario
from olds_files.recetas_categorias import crear_tabla_categorias, crear_tabla_recetas, registrar_categoria, registrar_receta
from olds_files.likes_sistema import add_user, add_receta, like, unlike, count
from olds_files.ver_usuarios import ver_usuarios

if __name__ == "__main__":
    # Crear tablas
    crear_tabla_usuarios()
    crear_tabla_categorias()
    crear_tabla_recetas()

    # Crear categorías base
    registrar_categoria("Vegetariano")
    registrar_categoria("Keto")
    registrar_categoria("Postres")

    # Registrar usuario de prueba
    registrar_usuario("Alayna", "alayna@email.com", "1234")

    # Ver usuarios
    ver_usuarios()

    # Registrar receta de prueba
    registrar_receta()

    # Prueba de likes
    add_user("Bernie")
    add_receta("Arroz")
    like("Bernie", 1)
    count(1)
    unlike("Bernie", 1)
    count(1)