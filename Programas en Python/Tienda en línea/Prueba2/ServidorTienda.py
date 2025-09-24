import socket, json
from Producto import obtenerRuta, guardarArticulos

rutaJSON = obtenerRuta() # Obetenos la ruta del archivo JSON, donde se guardan los artículos
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creamos el socket (IPv4, TCP)
server.bind(("127.0.0.1", 5000)) # Conectamos el servidor a la IP y al puerto
server.listen(2) # El socket esta en modo servidor, (1) = Espera una solicitud en cola 

print("Servidor en espera de clientes...")

while (True):
    conn, addr = server.accept() # Espera hasta que un cliente se conecte
    print(f"\nCliente conectado desde: {addr}")

    # Recibir solicitud desde el cliente
    pedido = conn.recv(4096).decode() # Servidor espera a recibir algo
    print(f"\nSe recibe desde el cliente: {pedido}")
    solicitud = json.loads(pedido) # Obtenemos la solicitud desde el cliente

    if (solicitud["accion"] == "LISTAR_ARTICULOS"): # Listar artículos
        articulos = guardarArticulos(rutaJSON) # Guardamos los artículos en un diccionario
        print(f"\nSe envia al cliente: {articulos}")
        respuesta = json.dumps(articulos).encode("utf-8") # Serializar el JSON
        conn.send(respuesta) # Lo envia al cliente
    else:
        conn.send(b"Comando no reconocido")

    conn.close() # Cerrar la conexión con el cliente