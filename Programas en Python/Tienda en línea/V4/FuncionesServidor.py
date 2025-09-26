import os

def obtenerRuta() -> tuple[str, str]:
    """
    Obtiene la ruta del archivo "articulos.json".

    Esta función construye la ruta completa hacia el archivo "articulos.json".

    Returns
    -------
    tuple
        (rutaArticulos, rutaCarrito)

        - **rutaArticulos** (str): Ruta completa del archivo "Articulos.json".
        - **rutaCarrito** (str): Ruta completa del archivo "Carrito.json".
    """
    carpetaScript = os.path.dirname(os.path.abspath(__file__)) # Obtiene la ruta de la carpeta del script
    rutaArticulos = os.path.join(carpetaScript, "articulos.json") # Construye la ruta completa hacia "Articulos.json"
    rutaCarrito = os.path.join(carpetaScript, "Carrito.json") # Construye la ruta completa hacia "Carrito.json"
    
    return rutaArticulos, rutaCarrito
