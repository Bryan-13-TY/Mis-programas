import socket

# Crear el socket (AF_INET = IPv4, SOCK_STREAM = TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Reusar puerto para evitar errores al reiniciar
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Asociar el socket a una IP y un puerto
server_socket.bind(("127.0.0.1", 5000))

# Poner el servidor en modo escucha
server_socket.listen()

print("Servidor en espera de conexiones...")

while (True):
    # Bloquea aquí hasta que llegue un cliente
    client_socket, addr = server_socket.accept()
    print(f"Conexión desde {addr}")

    # Bloque aquí hasta recibir datos
    data = client_socket.recv(1024).decode()
    print(f"Cliente dice: {data}")

    # Enviar respuesta
    client_socket.send("Hola cliente!".encode())

    # Cerrar conexión
    client_socket.close()