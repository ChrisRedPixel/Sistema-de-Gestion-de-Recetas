from db import crear_tablas
from usuarios import registrar_usuario
from categorias import registrar_categoria
from recetas import registrar_receta
from likes import like, unlike, contar_likes
from ver_usuarios import ver_usuarios

if __name__ == "__main__":
    crear_tablas()

    # Categorías base
    registrar_categoria("Vegetariano")
    registrar_categoria("Keto")
    registrar_categoria("Postres")

    # Usuario
    registrar_usuario("Alayna", "alayna@email.com", "1234")

    # Ver usuarios
    ver_usuarios()

    # Crear receta (usuario ID 1)
    registrar_receta(1)

    # Likes
    like(1, 1)
    contar_likes(1)
    unlike(1, 1)
    contar_likes(1)