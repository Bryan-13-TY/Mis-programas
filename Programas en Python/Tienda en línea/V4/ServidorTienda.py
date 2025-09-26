import socket, json
from FuncionesServidor import obtenerRuta

rutaArticulos, rutaCarrito = obtenerRuta() # Obetenos las rutas de los archivos JSON (Articulos.json, Carrito.json)

# Cremos el servisor y lo conectamos al cliente
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creamos al servidor (dirección IPv4, protocolo TCP)
servidor.bind(("127.0.0.1", 5000)) # Conectamos el servidor a la IP y al puerto
servidor.listen(2) # El socket esta en modo servidor, (2) = espera una solicitud en cola

print(">> Servidor en espera de clientes...")

# Aquí empieza el servidor a operar
while (True): # El servidor simpre acivo
    conn, addr = servidor.accept() # Espeta que un cliente se conecte al socket del servidor (conexión con cliente, dirección del cliente)

    print(f"\n>> Cliente conectado desde: {addr}")

    while (True): # Se mantiene la conexión abierta con el cliente
        # Verificamos la conexión con el cliente
        try:
            pedido = conn.recv(4096).decode() # Recibimos la solicitud del cliente

            # Verificamos si la solicitud llego
            if not pedido:
                print("\n>> Cliente desconectado")

                break

            print(f"\n>> Se recibe desde el cliente la solicitud: {pedido}")

            # Intentamos interpretar la solicitud del cliente (JSON) 
            try:
                solicitud = json.loads(pedido) # Convierte la solicitud en JSON a un diccionario
            except json.JSONDecodeError:
                conn.send(b"Solicitud no valida")

                continue

        except:
