import socket, json
from Producto import obtenerRuta, guardarArticulos

rutaJSON = obtenerRuta() # Obetenos la ruta del archivo JSON, donde se guardan los artículos
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creamos el socket (IPv4, TCP)
server.bind(("127.0.0.1", 5000)) # Conectamos el servidor a la IP y al puerto
server.listen(2) # El socket esta en modo servidor, (1) = Espera una solicitud en cola 

print("Servidor en espera de clientes...")

while True:
    conn, addr = server.accept() # Espera hasta que un cliente se conecte
    print("Cliente conectado desde:", addr)

    # Recibir solicitud desde el cliente
    request = conn.recv(4096).decode() # Servidor espera a recibir algo
    print("Solicitud:", request)
    solicitud = json.loads(request) # Obtenemos la solicitud desde el cliente

    if request == "LISTAR_ARTICULOS": # Listar artículos
        articulos = guardarArticulos(rutaJSON) # Guardamos los artículos en un diccionario
        # Serializar a JSON y enviar
        response = json.dumps(articulos).encode("utf-8") # Serializar el JSON
        conn.send(response) # Lo envia al cliente
    elif solicitud["accion"] == "BUSCAR_ARTICULOS": # Buscar artículos por nombre o marca
        valor = solicitud["valor"].lower() # Guardamos la marca o el nombre del artículo

        # Buscamo el artículo en la lista
        encontrados = [
            art for art in articulos["articulos"]
            if valor in art["nombre"].lower() or valor in art["marca"].lower()
        ]

        # Preparamos la respuesta para enviarse
        if encontrados:
            respuesta = {"articulos": encontrados}
        else:
            respuesta = {"error": f"No se encontraron artículos que coincidan con '{solicitud['valor']}'"}

        conn.send(json.dumps(respuesta).encode("utf-8")) # Serializar el JSON
    else:
        conn.send(b"Comando no reconocido")

    conn.close() # Cerrar el servidor