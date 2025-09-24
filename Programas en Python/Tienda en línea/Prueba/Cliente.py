import socket

# Crear socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bloquea aquí hasta conectarse
client_socket.connect(("127.0.0.1", 5000))

# Enviar mensaje
client_socket.send("Hola servidor!".encode())

# Bloquea aquí hasta que el servidor responda
data = client_socket.recv(1024).decode()
print(f"Servidor responde: {data}")

# Cerrar la conexión
client_socket.close()