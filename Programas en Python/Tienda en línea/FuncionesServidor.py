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

def cargarJSON(ruta: str) -> dict:
    """
    Convierte los artículos del archivo "Articulos.json" o "Carrito.json" a un diccionario.

    Esta función lee el archivo "Articulos.json" con codificación UTF-8, guarda el objeto
    archivo en "file" y lo convierte a un objeto de tipo Pyhton, es decir; a un diccionario.

    Parameters
    ----------
    ruta : str
        Ruta hacia el archivo "Articulos.json" o "Carrito.json".

    Returns
    -------
    dict
        Diccionario con los artículos guardados del archivo "Articulos.json" o "Carrito.json.
    """
    with open(ruta, "r", encoding = "utf-8") as file:
        articulos = json.load(file) # Toma "file" y lo convierte a un objeto de tipo Python (deserialización)

    return articulos

def guardarJSON(rutaCarrito: str, articulo: dict) -> None:
    """
    Parameters
    ----------
    rutaCarrito : str
        Ruta hacia el archivo "Carrito.json".
    articulos: dict
        Diccionario con el artículo a agregar al carrito.
    """
    with open(rutaCarrito, "w", encoding = "utf-8") as file:
        json.dump(articulo, file, indent = 4, ensure_ascii = False)


def enviarMensaje(mensaje: str, conexion: socket.socket) -> None:
    mensajeEnviar = {"mensaje": [{"error": f"{mensaje}"}]} # Se crea el JSON con el mensaje de error

    print(f"\n>> Se envia al cliente: {mensajeEnviar}") # Se imprime lo que se envía al cliente

    respuesta = json.dumps(mensajeEnviar).encode("utf-8") # Convierte el diccionario a una cadena en formato JSON (serialización) y luego a bytes
    conexion.send(respuesta) # Envía los bytes al cliente a traves del socket "conexion" 

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
    articulos = cargarJSON(ruta) # Obtenemos el diccionario con los artículos

    # Verificamos si hay artículos en la tienda o en el carrito
    if ("articulos" in articulos):
        if (not articulos["articulos"]): # Si no hay artículos en la tienda
            enviarMensaje("No hay artículos para mostrar", conexion)
        else:
            print(f"\n>> Se envia al cliente: {articulos}") # Se imprime lo que se envía al cliente

            respuesta = json.dumps(articulos).encode("utf-8") # Convierte el diccionario a una cadena en formato JSON (serialización) y luego a bytes
            conexion.send(respuesta) # Envía los bytes al cliente a traves del socket "conexion"

    if ("carrito" in articulos):
        if (not articulos["carrito"]): # Si no hay artículos en el carrito
            enviarMensaje("No hay artículos para mostrar", conexion)
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
    articulos = cargarJSON(rutaArticulos) # Guardamos los artículos en un diccionario
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
        enviarMensaje("No hay coincidencias", conexion)

def agregarCarrito(rutaArticulos: str, rutaCarrito: str, criterioBusqueda: str, cantidad: int, conexion: socket.socket) -> None:
    # Revisamos si el criterio de búsqueda fue el nombre o el id del artículo y ajustamos
    # el tipo de la varibale 'buscar'
    if (criterioBusqueda.isdigit()):
        buscar = int(criterioBusqueda)
    else:
        buscar = criterioBusqueda.lower()

    articulos = cargarJSON(rutaArticulos) # Guardamos los artículos en un diccionario
    carrito = cargarJSON(rutaCarrito) # Guardamos los artículos del carrito en un diccionario

    articuloAgregar = None # Aquí se guarda el artículo a agregar

    # Buscamos el artículo a agregar
    for art in articulos.get("articulos", []):
        if (isinstance(buscar, int) and buscar == art["id"]):
            articuloAgregar = art

            break
        elif (isinstance(buscar, str) and buscar in art["nombre"].lower()):
            articuloAgregar = art

            break

    # Verificamos que se haya encontrado el artículo
    if (not articuloAgregar):
        enviarMensaje("El artículo no existe en la tienda", conexion)
        
        return

    # Verificamos si el stock del artículo es suficiente
    if (cantidad > articuloAgregar["stock"]):
        enviarMensaje(f"No hay suficiente stock para agregar {cantidad} artículos", conexion)
        
        return
    
    # Verificamos si el artículo encontrado ya esta en el artículo
    for item in carrito["carrito"]:
        if (item["id"] == articuloAgregar["id"]): # Si ya esta el artículo en el carrito
            if (item["cantidad"] + cantidad > 5): # Si es menor qur 5
                enviarMensaje("No pudes agregar más de cinco unidades del mismo artículo", conexion)

                return
            
            item["cantidad"] += cantidad # Actualizamos la cantidad del artículo en el carrito
            item["precioTotal"] = item["precio"] * item["cantidad"] # Actualizamos el precio total del artículo

            guardarJSON(rutaCarrito, carrito) # Actualizamos el artíclo en el carrito
            enviarMensaje("El artículo se actualizó en el carrito", conexion)

            return
        
    # Se crea el artículo que se va a agregar al carrito, si este no existe previamente
    itemCarrito = articuloAgregar.copy()
    itemCarrito.pop("stock", None) # Se saca el item none del artículo a agregar
    itemCarrito["cantidad"] = cantidad # Se crea el item 'cantidad' en el artículo a agregar
    itemCarrito["precioTotal"] = itemCarrito["precio"] * cantidad # Se calcula el precio total y se cre el item 'precioTotal' en el artículo a agregar

    carrito["carrito"].append(itemCarrito) # Se agregan los items creados al artículo a agregars
    guardarJSON(rutaCarrito, carrito) # Se agrega el artículo al carrito
    enviarMensaje("El artículo se agregó al carrito", conexion)

def eliminarCarrito(rutaCarrito: str, criterioBusqueda: str, cantidad: int, conexion: socket.socket) -> None:
    # Revisamos si el criterio de búsqueda fue el nombre o el id del artículo y ajustamos
    # el tipo de la varibale 'buscar'
    if (criterioBusqueda.isdigit()):
        buscar = int(criterioBusqueda)
    else:
        buscar = criterioBusqueda.lower()

    carrito = cargarJSON(rutaCarrito) # Guardamos los artículos del carrito en un diccionario

    articuloEliminar = None # Aquí se guarda el artículo a eliminar

    # Buscamos el artículo a eliminar
    for art in carrito.get("carrito", []):
        if (isinstance(buscar, int) and buscar == art["id"]):
            articuloEliminar = art

            break
        elif (isinstance(buscar, str) and buscar in art["nombre"].lower()):
            articuloEliminar = art

            break

    # Verificamos que se haya encontrado el artículo
    if (not articuloEliminar):
        enviarMensaje("El artículo no existe en el carrito", conexion)
        
        return
    
    # Verificamos si la cantidad del artículo es suficiente
    if (cantidad > articuloEliminar["cantidad"]):
        enviarMensaje(f"No hay suficiente artículos para eliminar {cantidad} artículos", conexion)
        
        return
    
    # Verificamos si el artículo encontrado ya esta en el carrito
    for item in carrito["carrito"]:
        if (item["id"] == articuloEliminar["id"]): # Si ya esta el artículo en el carrito
            if ((item["cantidad"] - cantidad) > 0): # Si todavía restan artículos en el carrito
                item["cantidad"] -= cantidad # Actualizamos la cantidad del artículo en el carrito
                item["precioTotal"] = item["precio"] * item["cantidad"] # Actualizamos el precio total del artículo

                guardarJSON(rutaCarrito, carrito) # Actualizamos el artíclo en el carrito
                enviarMensaje("El artículo se actualizó en el carrito", conexion)
            else: # Ya no hay artículos
                carrito["carrito"].remove(item) # Eliminamos el artículo del carrito
                
                guardarJSON(rutaCarrito, carrito) # Actualizamos el artíclo en el carrito
                enviarMensaje("El artículo se eliminó del carrito", conexion)

            return

def finalizarCompra():
    print