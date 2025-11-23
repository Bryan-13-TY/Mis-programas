import socket

HOST = "127.0.0.1" # Localhost
PORT = 8080

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen(5)

    print(f"Servidor escuchando en http://{HOST}:{PORT}")

    while True:
        cliente, direccion = servidor.accept()
        print(f"Conexión de: {direccion}")

        # Recibir petición HTTP
        peticion = cliente.recv(1024).decode("utf-8")
        print("\n--- PETICIÓN ---")
        print(peticion)

        # Solo respondemos GET por ahora
        if peticion.startswith("GET"):
            # Respuesta HTTP mínina
            respuesta = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                "\r\n"
                "<html>"
                "<head><title>Mi servidor</title></head>"
                "<body>"
                "<h1>Servidor HTTP funcionando</h1>"
                "<p>¡Lo lograste!</p>"
                "</body>"
                "</html>"
            )
        else:
            respuesta = (
                "HTTP/1.1 405 Method Not Allowed\r\n"
                "Content-Type: text/plain\r\n"
                "\r\n"
                "Método no permitido"
            )

        # Enviar respuesta
        cliente.sendall(respuesta.encode("utf-8"))

        # Cerrar conexión

if __name__ == "__main__":
    iniciar_servidor()