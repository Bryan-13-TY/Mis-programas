import os, json

def obtenerRuta() -> str:
    """
    Obtiene la ruta del archivo "articulos.json".

    Esta función construye la ruta completa hacia el archivo "articulos.json".

    Returns
    -------
    str
        Ruta completa del archivo "articulos.json".
    """
    carpetaScript = os.path.dirname(os.path.abspath(__file__)) # Obtiene la ruta de la carpeta del script
    rutaArticulos = os.path.join(carpetaScript, "articulos.json") # Construye la ruta completa hacia "articulos.json"
    rutaCarrito = os.path.join(carpetaScript, "Carrito.json")
    return rutaArticulos, rutaCarrito

def actualizarJSON(rutaArticulos: str, data) -> None:
    with open(rutaArticulos, "w", encoding = "utf-8") as file:
        json.dump(data, file, indent = 4, ensure_ascii = False)

def guardarArticulos(ruta: str) -> dict:
    """
    Convierte los artículos del archivo "Articulos.json" o "Carrito.json" a un diccionario.

    Esta función lee el archivo "Articulos.json" con codificación UTF-8, guarda el objeto
    archivo en "file" y lo convierte a un objeto de tipo Pyhton, es decir; a un diccionario.

    Parameters
    ----------
    rutaArticulos : str
        Ruta hacia del archivo "Articulos.json" o "Carrito.json".

    Returns
    -------
    dict
        Diccionario con los artículos guardados del archivo "Articulos.json" o "Carrito.json.
    """
    with open(ruta, "r", encoding = "utf-8") as file:
        articulos = json.load(file) # Toma "file" y lo convierte a un objeto de tipo Python (deserialización)

    return articulos

def mostrarCarrito(carrito: dict) -> None:
    ""
    print("Articulos en el carrito:")

    for art in carrito["carrito"]:
        print(f"\nId: {art['id']}")
        print(f"Nombre: {art['nombre']}")
        print(f"Precio: ${art['precio']} MXN")
        print(f"Marca: {art['marca']}")
        print(f"Stock: {art['stock']}")

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
    print("\nArículos(s) encontrados(s):")
    for msj in mensaje["mensaje"]:
        print(f"\n>> {msj['error']}")

def limpiarTerminal() -> None:
    """
    Limpia la terminal de cualquier sistema operativo. 
    """
    os.system('cls' if os .name == 'nt' else 'clear')