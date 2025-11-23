import socket
import os
from pathlib import Path

HOST = "127.0.0.1"
PORT = 8080
CARPETA = Path("archivos")

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

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen(5)

    print(f"Servidor escuchando en http://{HOST}:{PORT}")

    while True:
        cliente, direccion = servidor.accept()
        print(f"Conexión de: {direccion}")

        peticion = cliente.recv(1024).decode("utf-8", errors="ignore")
        print("\n--- PETICIÓN ---")
        print(peticion)

        if not peticion:
            cliente.close()
            continue

        # Línea principal: GET /archivo HTTP/1.1
        linea = peticion.splitlines()[0]
        metodo, ruta, _ = linea.split()

        if metodo != "GET":
            respuesta = (
                "HTTP/1.1 405 Method Not Allowed\r\n"
                "Content-Type: text/plain\r\n\r\n"
                "Metodo no permitido"
            )
            cliente.sendall(respuesta.encode())
            cliente.close()
            continue

        if ruta == "/":
            ruta = "/index.html"

        archivo = CARPETA / ruta.lstrip("/")

        if archivo.exists() and archivo.is_file():
            contenido = archivo.read_bytes()
            mime = obtener_mime(archivo)
            
            cabecera = (
                "HTTP/1.1 200 OK\r\n"
                f"Content-Type: {mime}\r\n"
                f"Content-Length: {len(contenido)}\r\n"
                "\r\n"
            ).encode()

            cliente.sendall(cabecera + contenido)
        
        else:
            respuesta = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/html\r\n\r\n"
                "<h1>404 - Archivo no encontrado</h1>"
            )
            cliente.sendall(respuesta.encode())

        cliente.close()

if __name__ == "__main__":
    iniciar_servidor()