"""
Archivo 'servidor.py': Este archivo implementa un servidor HTTP en python usando
sockets y threading, con estas características:

    - Atiende peticiones HTTP en el puerto 8080 (servidor primario)
    - Si hay demasidas conexiones, inicia automáticamente un segundo servidor en el 8081
    - Soporta los metodos:
        - GET -> leer archivos
        - POST -> crear archivos
        - PUT -> actualizar archivos
        - DELETE -> eliminar archivos
    - Usa un pool de conexiones máximo de 10
    - Genera un ID único (UUID) por conexión
    - Muestra hora, ID y estado en consola
    - Guarda los archivos en diferentes carpetas según el servidor:
        - archivos_1 (8080)
        - archivos_2 (8081) 

Autores:
    - García Escamilla Bryan Alexis
    - Meléndez Macedonio Rodrigo

Fecha: 23/11/2025
"""
import socket
import threading
import time
import uuid # para generar ID único por conexión
from datetime import datetime
from pathlib import Path

import utils

HOST = "127.0.0.1"

# Puertos
PUERTO_PRIMARIO = 8080
PUERTO_SECUNDARIO = 8081

# Capetas
CARPETA_SCRIPT = Path(__file__).parent
CARPETA_PRIMARIA = CARPETA_SCRIPT / "archivos_1"
CARPETA_SECUNDARIA = CARPETA_SCRIPT / "archivos_2"

CARPETA_PRIMARIA.mkdir(exist_ok=True)
CARPETA_SECUNDARIA.mkdir(exist_ok=True)

# Pool
POOL_MAX = 10 # tamaño lógico del pool
MITAD_POOL = POOL_MAX // 2 # umbral para el segundo servidor

conexiones_activas = 0
lock = threading.Lock() # evita que varios hilos modifiquen el contador al mismo tiempo

# flag para evitar arrancar el servidor secundario más de una vez
segundo_servidor_iniciado = False # FIXME se modifica sin lock

MIME_TYPES = {
    ".html": "text/html",
    ".json": "application/json",
    ".txt": "text/plain",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
}

def ahora() -> str:
    """
    Devuelve la hora actual formateada. Se usa para estampar timestamp en los logs.
    
    Returns
    -------
    str
        Fecha y hora actual en formato legibe.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def obtener_mime(archivo: Path) -> str:
    """
    Devuleve el tipo de MIME según la extensión.

    Parameters
    ----------
    archivos : Path
        Ruta del archivo.

    Returns
    -------
    str
        MIME correspondiente, de lo contrarios un MIME genérico.
    """
    return MIME_TYPES.get(archivo.suffix, "application/octet-stream")


def leer_body(peticion: str) -> str:
    """
    Extrae el body real de la petición.
    
    Parameters
    ----------
    peticion : str
        Petición HTTP (headers + body).

    Returns
    -------
    str
        Cuerpo de la petición, de lo contrario una cadena vacía.
    """
    separador = "\r\n\r\n" # para separar el encabezado del cuerpo

    if separador in peticion:
        return peticion.split(separador, 1)[1] # devuelve el cuerpo de la petición 
    
    return ""


def procesar_peticion(cliente: socket.socket, peticion: str, carpeta_base: Path, puerto: int):
    """
    Interpreta la primera línea de la petición y ejecuta comportamiento por método.

    Parameters
    ----------
    cliente : socket.socket
        El socket del navegador/curl.
    peticion : str
        El texto completo HTTP (headers + body).
    carpeta_base : Path
        Carpeta para el primer servidor donde guardar/buscar archivos.
    puerto : int
        Puerto del servidor: 8080 o 8081.
    """
    linea = peticion.splitlines()[0] # ej. 'GET /mensaje.txt HTTP/1.1'
    metodo, ruta, _ = linea.split() # FIXME no hay manejo de errores si la petición está mal formada

    if ruta == "/": 
        ruta = "/index.html" # se redirige a index.html

    archivo = carpeta_base / ruta.lstrip("/") # ruta completa al recurso en la carpeta base

    # ====== GET ======
    if metodo == "GET":
        if archivo.exists() and archivo.is_file(): 
            contenido = archivo.read_bytes() # lee los bytes del contenido del archivo
            mime = obtener_mime(archivo)

            cabecera = (
                "HTTP/1.1 200 OK\r\n"
                f"Content-Type: {mime}\r\n"
                f"Content-Length: {len(contenido)}\r\n" # se calcula el tamaño del contenido
                "\r\n"
            ).encode()

            print("-"*50)
            print(f"{utils.BLUE}--- RESPUESTA ({puerto}) ---{utils.RESET}")
            print(cabecera.decode(errors="ignore"))
            print("-"*50)

            cliente.sendall(cabecera + contenido)
        else:
            respuesta = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/html\r\n\r\n"
                "<h1>404 - Archivo no encontrado</h1>"
            )

            print("-"*50)
            print(f"{utils.BLUE}--- RESPUESTA ({puerto}) ---{utils.RESET}")
            print(respuesta)
            print("-"*50)
            
            cliente.sendall(respuesta.encode())

    # ====== POST ======
    elif metodo == "POST":
        body = leer_body(peticion) # se extrae el cuerpo de la petición

        archivo.write_text(body, encoding="utf-8") # escribe el contenido como texto (se crea el archivo o lo sobrescribe)

        respuesta = ( # FIXME no se incluye 'Content-Length'
            "HTTP/1.1 201 Created\r\n"
            "Content-Type: text/plain\r\n\r\n"
            f"Archivo {archivo.name} creado correctamente en {carpeta_base}"
        )

        print("-"*50)
        print(f"{utils.BLUE}--- RESPUESTA ({puerto}) ---{utils.RESET}")
        print(respuesta)
        print("-"*50)

        cliente.sendall(respuesta.encode())

    # ====== PUT ======
    elif metodo == "PUT":
        body = leer_body(peticion) # se extrae el cuerpo de la petición

        if archivo.exists():
            archivo.write_text(body, encoding="utf-8") # sobrescribe el contenido del archivo

            respuesta = ( # FIXME no se incluye 'Content-Length'
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n\r\n"
                f"Archivo {archivo.name} actualizado correctamente"
            )
        else:
            respuesta = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/plain\r\n\r\n"
                "Archivo no existe"
            )

        print("-"*50)
        print(f"{utils.BLUE}--- RESPUESTA ({puerto}) ---{utils.RESET}")
        print(respuesta)
        print("-"*50)

        cliente.sendall(respuesta.encode())

    # ====== DELETE ======
    elif metodo == "DELETE":
        if archivo.exists():
            archivo.unlink() # se borra el archivo

            respuesta = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n\r\n"
                f"Archivo {archivo.name} eliminado"
            )
        else:
            respuesta = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/plain\r\n\r\n"
                "Archivo no encontrado"
            )

        print("-"*50)
        print(f"{utils.BLUE}--- RESPUESTA ({puerto}) ---{utils.RESET}")
        print(respuesta)
        print("-"*50)

        cliente.sendall(respuesta.encode())

    # ====== OTROS ======
    else: # el método no se soporta
        respuesta = (
            "HTTP/1.1 405 Not Allowed\r\n"
            "Content-Type: text/plain\r\n\r\n"
            "Metodo no permitido"
        )

        print("-"*50)
        print(f"{utils.BLUE}--- RESPUESTA ({puerto}) ---{utils.RESET}")
        print(respuesta)
        print("-"*50)

        cliente.sendall(respuesta.encode())


def atender_cliente(cliente: socket.socket, direccion: tuple[str, int], carpeta_base: Path, puerto: int):
    """
    Parameters
    ----------
    cliente : socket.socket
        Socket conectado.
    direccion : tuple
        Dirección del cliente .
    carpeta_base : Path
        Carpeta correspondiente.
    """
    global conexiones_activas

    conexion_id = uuid.uuid4().hex[:8]# ID único para esta conexión

    with lock: # se protege el incremento del contador
        conexiones_activas += 1
        print(f"[{ahora()}] [+] [ID: {conexion_id}] ({puerto}) Conexiones activas: {conexiones_activas}")

    try:
        datos = cliente.recv(4096) # FIXME se asume que la petición (headers + body) cabe en 4096 bytes
        peticion = datos.decode("utf-8", errors="ignore")

        if not peticion:
            return
        
        # mostrar petición
        linea = peticion.splitlines()[0]
        print(f"[{ahora()}] [ID: {conexion_id}] PETICIÓN => {linea}")
        
        # si se superó la mitad del pool, redirigir al servidor 2
        if conexiones_activas > MITAD_POOL and puerto == PUERTO_PRIMARIO:
            respuesta = (
                "HTTP/1.1 302 Found\r\n"
                f"Location: http://{HOST}:{PUERTO_SECUNDARIO}\r\n\r\n"
            )

            cliente.sendall(respuesta.encode())
            print(f"[{ahora()}] [ID: {conexion_id}] REDIRECCIONANDO A PUERTO {PUERTO_SECUNDARIO}")
            return
        
        procesar_peticion(cliente, peticion, carpeta_base, puerto)

        # log de respuesta
        print(f"[{ahora()}] [ID: {conexion_id}] RESPUESTA enviada correctamente")
        time.sleep(2) # para pruebas del pool
    except Exception as e:
        print(f"[{ahora()}] [ID: {conexion_id}] ERROR: {e}")

    finally:
        cliente.close()

        with lock:
            conexiones_activas -= 1
            print(f"[{ahora()}] [-] [ID: {conexion_id}] ({puerto}) Conexiones activas: {conexiones_activas}")


def iniciar_servidor(puerto: int, carpeta_base: Path):
    """
    Monta un servidor en el puerto indicado y sirve archivos desde la carpeta base.

    Parameters
    ----------
    puerto : int
        Puerto del servidor.
    carpeta_base : Path
        Carpeta de arcivos para el servidor.
    """
    global segundo_servidor_iniciado

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, puerto))
    servidor.listen()

    print(f"Servidor escuchando en http://{HOST}:{puerto} usando {carpeta_base}")

    while True:
        cliente, direccion = servidor.accept() # bloquea hasta que llega una conexión

        # si se supera la mitad del pool y no está activo el segundo servidor
        if conexiones_activas >= MITAD_POOL and not segundo_servidor_iniciado and puerto == PUERTO_PRIMARIO:
            print(f"\n{utils.RED}>>> INICIANDO SEGUNDO SERVIDOR (8081) <<<{utils.RESET}\n")

            threading.Thread(target=iniciar_servidor, args=(PUERTO_SECUNDARIO, CARPETA_SECUNDARIA), daemon=True).start()
            segundo_servidor_iniciado = True
        
        hilo = threading.Thread(target=atender_cliente, args=(cliente, direccion, carpeta_base, puerto))
        hilo.start()

if __name__ == "__main__":
    iniciar_servidor(PUERTO_PRIMARIO, CARPETA_PRIMARIA)