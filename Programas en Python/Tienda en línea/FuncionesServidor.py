import os, json, socket

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

def guardarArticulos(ruta: str) -> dict:
    """
    Convierte los artículos del archivo "Articulos.json" o "Carrito.json" a un diccionario.

    Esta función lee el archivo "Articulos.json" con codificación UTF-8, guarda el objeto
    archivo en "file" y lo convierte a un objeto de tipo Pyhton, es decir; a un diccionario.

    Parameters
    ----------
    ruta : str
        Ruta hacia del archivo "Articulos.json" o "Carrito.json".

    Returns
    -------
    dict
        Diccionario con los artículos guardados del archivo "Articulos.json" o "Carrito.json.
    """
    with open(ruta, "r", encoding = "utf-8") as file:
        articulos = json.load(file) # Toma "file" y lo convierte a un objeto de tipo Python (deserialización)

    return articulos

def listarArticulos(ruta: str, conexion: socket.socket) -> None:
    """
    Lista los artículos de la tienda o del carrito de compras.

    Esta función veriica si hay artículos en la tienda o en el carrito de compras,
    si los hay, los lista de lo contrario envía un mensaje de error.

    Parameters
    ----------
    ruta : str
        Ruta del archivo "Articulos.json" o "Carrito.json".
    conexion : socket.socket
        Nuevo socket que representa la conexión con un cliente en particular.
    """
    articulos = guardarArticulos(ruta) # Obtenemos el diccionario con los artículos

    # Verificamos si hay artículos en la tienda o en el carrito
    if ("articulos" in articulos):
        if (not articulos["articulos"]): # Si no hay artículos en la tienda
            mensaje = {"mensaje": [{"error": "No hay artículos para mostrar"}]} # Se crea el JSON con el mensaje de error

            print(f"\n>> Se envia al cliente: {mensaje}") # Se imprime lo que se envía al cliente
            
            respuesta = json.dumps(mensaje).encode("utf-8") # Convierte el diccionario a una cadena en formato JSON (serialización) y luego a bytes
            conexion.send(respuesta) # Envía los bytes al cliente a traves del socket "conexion"
        else:
            print(f"\n>> Se envia al cliente: {articulos}") # Se imprime lo que se envía al cliente

            respuesta = json.dumps(articulos).encode("utf-8") # Convierte el diccionario a una cadena en formato JSON (serialización) y luego a bytes
            conexion.send(respuesta) # Envía los bytes al cliente a traves del socket "conexion"

    if ("carrito" in articulos):
        if (not articulos["carrito"]): # Si no hay artículos en el carrito
            mensaje = {"mensaje": [{"error": "No hay artículos para mostrar"}]} # Se crea el JSON con el mensaje de error

            print(f"\n>> Se envia al cliente: {mensaje}") # Se imprime lo que se envía al cliente
            
            respuesta = json.dumps(mensaje).encode("utf-8") # Convierte el diccionario a una cadena en formato JSON (serialización) y luego a bytes
            conexion.send(respuesta) # Envía los bytes al cliente a traves del socket "conexion"
        else:
            print(f"\n>> Se envia al cliente: {articulos}") # Se imprime lo que se envía al cliente

            respuesta = json.dumps(articulos).encode("utf-8") # Convierte el diccionario a una cadena en formato JSON (serialización) y luego a bytes
            conexion.send(respuesta) # Envía los bytes al cliente a traves del socket "conexion"

def buscarArticulo(rutaArticulos: str, criterioBusqueda: str, conexion: socket.socket) -> None:
    """
    Busca un artículo que coincida con el nombre o marca indicada por el usaurio.

    Esta función busca en los artículos de la tiendo aquel o aquellos que coincidan con la
    marca o nombre de un artículo. Si se encuentra una coincidencia agrega e artículo a un JSON,
    de lo contrario se envía el mensaje correspondiente.

    Parameters
    ----------
    rutaArticulos : str
        Ruta hacia del archivo "Articulos.json".
    criterioBusqueda : str
        La marca o el nombre del artículo a buscar.
    conexion : socket.socket
        Nuevo socket que representa la conexión con un cliente en particular.
    """
    buscar = criterioBusqueda.lower() # Guardamos el nombre o marca del artículo
    articulos = guardarArticulos(rutaArticulos) # Guardamos los artículos en un diccionario
    counter = 0 # Contador de artículos encontrados

    coincidencias = {"articulos": []} # Cremos el JSON con un diccionario vacío

    for art in articulos.get("articulos", []): # Buscamos los artículos
        if ((buscar in art["nombre"].lower()) or (buscar in art["marca"].lower())):
            coincidencias["articulos"].append(art) # Agregamos el artículo que coindice con la búsqueda
            counter += 1

    if (counter > 0): # Si se encontró al menos un artículo
        print(f"\n>> Se envia al cliente: {coincidencias}") # Se imprime lo que se envía al cliente

        respuesta = json.dumps(coincidencias).encode("utf-8") # Serializar el JSON
        conexion.send(respuesta)
    else: # Si no se encontro ningún artículo
        mensaje = {"mensaje": [{"error": "No hay coincidencias"}]} # Se crea el JSON con el mensaje

        print(f"\n>> Se envia al cliente: {mensaje}") # Se imprime lo que se envía al cliente

        respuesta = json.dumps(mensaje).encode("utf-8") # Serializar el JSON
        conexion.send(respuesta) # Se envía la respuesta al cliente

def agregarCarrito(rutaArticulos: str, rutaCarrito: str, criterioBusqueda: str, cantidad: int) -> None:
    # Revisamos se el criterio de búsqueda fue el nombre o el id del artículo
    if (criterioBusqueda.isdigit()):
        buscar = int(criterioBusqueda)
    else:
        buscar = criterioBusqueda

    articulos = guardarArticulos(rutaArticulos) # Guardamos los artículos en un diccionario
    carrito = guardarArticulos(rutaCarrito) # Guardamos los artículos del carrito en un diccionario

    # Buscamos el artículo a agregar
    for art in articulos.get("articulos", []):
        if (isinstance(buscar, int) and buscar == art["id"]):
            print(f"El elemento a agregar es: {art}")
        elif (isinstance(buscar, str) and buscar in art["nombre"]):
            print(f"El elemento a agregar es: {art}")

def eliminarCarrito():
    print

def finalizarCompra():
    print