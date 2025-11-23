import socket
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

def leer_body(peticion: str) -> str:
    separador = "\r\n\r\n"

    if separador in peticion:
        return peticion.split(separador, 1)[1]
    
    return ""

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen(5)

    print(f"Servidor escuchando en http://{HOST}:{PORT}")

    while True:
        try:
            cliente, direccion = servidor.accept()
            print(f"Conexión de: {direccion}")

            datos = cliente.recv(4096)
            peticion = datos.decode("utf-8", errors="ignore")

            print("\n--- PETICIÓN ---")
            print(peticion)

            if not peticion:
                cliente.close()
                continue

            # Ejemplo: POST /nuevo.txt HTTP/1.1
            linea = peticion.splitlines()[0]
            metodo, ruta, _ = linea.split()

            if ruta == "/":
                ruta = "/index.html"

            archivo = CARPETA / ruta.lstrip("/")
            
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

                    cliente.sendall(cabecera + contenido)
                else:
                    respuesta = (
                        "HTTP/1.1 404 Not Found\r\n"
                        "Content-Type: text/html\r\n\r\n"
                        "<h1>404 - Archivo no encontrado</h1>"
                    )
                    cliente.sendall(respuesta.encode())

            # ====== POST ======
            elif metodo == "POST":
                body = leer_body(peticion)

                with open(archivo, "w", encoding="utf-8") as f:
                    f.write(body)

                respuesta = (
                    "HTTP/1.1 201 Created\r\n"
                    "Content-Type: text/plain\r\n\r\n"
                    f"Archivo {archivo.name} creado correctamente"
                )
                cliente.sendall(respuesta.encode())

            # ====== PUT ======
            elif metodo == "PUT":
                body = leer_body(peticion)
                archivo.write_text(body, encoding="utf-8")

                respuesta = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/plain\r\n\r\n"
                    f"Archivo {archivo.name} actualizado correctamente"
                )
                cliente.sendall(respuesta.encode())

            # ===== DELETE ======
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
                
                cliente.sendall(respuesta.encode())

            # ====== OTROS ======
            else:
                respuesta = (
                    "HTTP/1.1 405 Not Allowed\r\n"
                    "Content-Type: text/plain\r\n\r\n"
                    "Metodo no permitido"
                )
                cliente.sendall(respuesta.encode())

            cliente.close()
        except Exception as e:
            print("Error:", e)
            cliente.close()

if __name__ == "__main__":
    iniciar_servidor()