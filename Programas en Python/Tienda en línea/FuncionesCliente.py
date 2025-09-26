import os, msvcrt

def listarTipo(articulos: dict, tipoArticulo: str) -> None:
    """
    Imprime todos los artículos del mismo tipo.

    Esta función recorre el diccionario con los artículos e imprime todos aquellos
    con el tipo "tipoArticulo" en un formato más legible.

    Parameters
    ----------
    articulos : dict
        Diccionario con los artículos.
    tipoArticulo: str
        Uno de los tipos de los artículos: "Abarrotes", "Bebidas", "Snacks", "Cuidado personal" y "Limpieza".
    """
    for art in articulos["articulos"]:
        if (art['tipo'] == tipoArticulo): # Si coincide con el tipo del artículo
            print(f"\nId: {art['id']}")
            print(f"Nombre: {art['nombre']}")
            print(f"Precio: ${art['precio']} MXN")
            print(f"Marca: {art['marca']}")
            print(f"Stock: {art['stock']} artículos disponibles")

def listarArticulos(articulos: dict) -> None:
    """
    Imprime todos los artículos de todos los tipos en formato más legible.

    Parameters
    ----------
    articulos: dict
        Diccionario con los artículos.
    """
    print("Lista de artículos de la tienda:\n")

    print("__Artículos de tipo Abarrotes__")
    listarTipo(articulos, "Abarrotes")
    print("\n__Artículos de tipo Bebidas__")
    listarTipo(articulos, "Bebidas")
    print("\n__Artículos de tipo Snacks__")
    listarTipo(articulos, "Snacks")
    print("\n__Artículos de tipo Cuidado personal__")
    listarTipo(articulos, "Cuidado personal")
    print("\n__Artículos de tipo Limpieza__")
    listarTipo(articulos, "Limpieza")

def limpiarTerminal() -> None:
    """
    Limpia la terminal de cualquier sistema operativo. 
    """
    os.system('cls' if os .name == 'nt' else 'clear')

def mostrarBusqueda(busqueda: dict) -> None:
    """
    Imprime los artículos resultantes después de la búsqueda por nombre o marca.

    Esta función recorre el diccionario con los artículos encontrados y los
    imprime en un formato más legible. 

    Parameters
    ----------
    busqueda: dict
        Diccionario con los artículos encontrados.
    """
    print("\nArtículo(s) encontrado(s):")
    for art in busqueda["articulos"]:
        print(f"\nId: {art['id']}")
        print(f"Tipo: {art['tipo']}")
        print(f"Nombre: {art['nombre']}")
        print(f"Precio: ${art['precio']} MXN")
        print(f"Marca: {art['marca']}")
        print(f"Stock: {art['stock']}")

def mostrarMensaje(mensaje: dict) -> None:
    """
    Imprime el mensaje guardado en el diccionario "mensaje".

    Parameters
    ----------
    mensaje : dict
        Diccionario de un solo elemento con el mensaje.
    """

    for msj in mensaje["mensaje"]:
        print(f">> {msj['error']}")

def mostrarCarrito(carrito: dict) -> None:
    """
    Imprime los artículos en el carrito de compras

    Parameters
    ----------
    carrito : dict
        Diccionario con los artículos del carrito de compras
    """
    print("Articulos en el carrito:")

    for art in carrito["carrito"]:
        print(f"\nId: {art['id']}")
        print(f"Nombre: {art['nombre']}")
        print(f"Precio: ${art['precio']} MXN")
        print(f"Marca: {art['marca']}")
        print(f"Stock: {art['stock']}")

def esperarTecla():
    return msvcrt.getch().decode("utf-8")  # devuelve la tecla como string