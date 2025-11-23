import socket
import threading
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
POOL_MAX = 10
MITAD_POOL = POOL_MAX // 2

conexiones_activas = 0
lock = threading.Lock()


segundo_servidor_iniciado = False

MIME_TYPES = {
    ".html": "text/html",
    ".json": "application/json",
    ".txt": "text/plain",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
}

def obtener_mime(archivo: Path) -> str:
    return MIME_TYPES.get(archivo.suffix, "application/octet-stream")


def leer_body(peticion: str) -> str:
    separador = "\r\n\r\n"

    if separador in peticion:
        return peticion.split(separador, 1)[1]
    
    return ""


def procesar_peticion(cliente: socket.socket, peticion: str, carpeta_base: Path, puerto: int):
    linea = peticion.splitlines()[0]
    metodo, ruta, _ = linea.split()

    if ruta == "/":
        ruta = "/index.html"

    archivo = carpeta_base / ruta.lstrip("/")

    # ====== GET ======
    if metodo == "GET":
        if archivo.exists() and archivo.is_file():
            contenido = archivo.read_bytes()
            mime = obtener_mime(archivo)

            cabecera = (
                "HTTP/1.1 200 OK\r\n"
                f"Content-Type: {mime}\r\n"
                f"Content-Length: {len(contenido)}\r\n"
                "\r\n"
            ).encode()

            print(f"\n{utils.BLUE}--- RESPUESTA ({puerto}) ---{utils.RESET}\n")
            print(cabecera.decode(errors="ignore"))

            cliente.sendall(cabecera + contenido)
        else:
            respuesta = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/html\r\n\r\n"
                "<h1>404 - Archivo no encontrado</h1>"
            )

            print(f"\n{utils.BLUE}--- RESPUESTA ({puerto}) ---{utils.RESET}\n")
            print(respuesta)
            
            cliente.sendall(respuesta.encode())
    # ====== POST ======
    elif metodo == "POST":
        body = leer_body(peticion)

        archivo.write_text(body, encoding="utf-8")

        respuesta = (
            "HTTP/1.1 201 Created\r\n"
            "Content-Type: text/plain\r\n\r\n"
            f"Archivo {archivo.name} creado correctamente en {carpeta_base}"
        )

        print(f"\n{utils.BLUE}--- RESPUESTA ({puerto}) ---{utils.RESET}\n")
        print(respuesta)

        cliente.sendall(respuesta.encode())

    # ====== PUT ======
    elif metodo == "PUT":
        body = leer_body(peticion)

        if archivo.exists():
            archivo.write_text(body, encoding="utf-8")

            respuesta = (
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

        print(f"\n{utils.BLUE}--- RESPUESTA ({puerto}) ---{utils.RESET}\n")
        print(respuesta)

        cliente.sendall(respuesta.encode())

    # ====== DELETE ======
    elif metodo == "DELETE":
        if archivo.exists():
            archivo.unlink()

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

        print(f"\n{utils.BLUE}--- RESPUESTA ({puerto}) ---{utils.RESET}\n")
        print(respuesta)

        cliente.sendall(respuesta.encode())

    # ====== OTROS ======
    else:
        respuesta = (
            "HTTP/1.1 405 Not Allowed\r\n"
            "Content-Type: text/plain\r\n\r\n"
            "Metodo no permitido"
        )

        print(f"\n{utils.BLUE}--- RESPUESTA ({puerto}) ---{utils.RESET}\n")
        print(respuesta)

        cliente.sendall(respuesta.encode())


def atender_cliente(cliente: socket.socket, direccion: str, carpeta_base: Path, puerto: int):
    global conexiones_activas

    with lock:
        conexiones_activas += 1
        print(f"[+] ({puerto}) Conexiones activas: {conexiones_activas}")

    try:
        datos = cliente.recv(4096)
        peticion = datos.decode("utf-8", errors="ignore")
        
        print("="*50)
        print(f"{utils.GREEN}PETICIÓN ({direccion} : puerto {puerto}){utils.RESET}")
        print(peticion)
        print("="*50)

        if not peticion:
            return
        
        # Si se superó la mitad del pool, redirigir al servidor 2
        if conexiones_activas > MITAD_POOL and puerto == PUERTO_PRIMARIO:
            respuesta = (
                "HTTP/1.1 302 Found\r\n"
                f"Location: http://{HOST}:{PUERTO_SECUNDARIO}\r\n\r\n"
            )

            cliente.sendall(respuesta.encode())
            return
        
        procesar_peticion(cliente, peticion, carpeta_base, puerto)
    except Exception as e:
        print("Error:", e)

    finally:
        cliente.close()

        with lock:
            conexiones_activas -= 1
            print(f"[-] ({puerto}) Conexiones activas: {conexiones_activas}")


def iniciar_servidor(puerto: int, carpeta_base: Path):
    global segundo_servidor_iniciado

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, puerto))
    servidor.listen()

    print(f"Servidor escuchando en http://{HOST}:{puerto} usando {carpeta_base}")

    while True:
        cliente, direccion = servidor.accept()

        # Si se supera la mitad del pool y no está activo el segundo servidor
        if conexiones_activas >= MITAD_POOL and not segundo_servidor_iniciado and puerto == PUERTO_PRIMARIO:
            print("\n>>> INICIANDO SEGUNDO SERVIDOR (8081) <<<\n")

            threading.Thread(target=iniciar_servidor, args=(PUERTO_SECUNDARIO, CARPETA_SECUNDARIA), daemon=True).start()
            segundo_servidor_iniciado = True
        
        hilo = threading.Thread(target=atender_cliente, args=(cliente, direccion, carpeta_base, puerto))
        hilo.start()

if __name__ == "__main__":
    iniciar_servidor(PUERTO_PRIMARIO, CARPETA_PRIMARIA)