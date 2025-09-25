import socket, json
from Producto import obtenerRuta, guardarArticulos

rutaJSON = obtenerRuta() # Obetenos la ruta del archivo JSON, donde se guardan los artículos
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creamos el socket (IPv4, TCP)
server.bind(("127.0.0.1", 5000)) # Conectamos el servidor a la IP y al puerto
server.listen(2) # El socket esta en modo servidor, (2) = Espera una solicitud en cola 

print(">> Servidor en espera de clientes...")

while (True):
    conn, addr = server.accept() # Espera hasta que un cliente se conecte
    print(f"\n>> Cliente conectado desde: {addr}")

    while (True): # Bucle para mantener la conexión abierta
        try: # Intentamos verificar si el cliente sigue conectado
            # Recibir solicitud desde el cliente
            pedido = conn.recv(4096).decode() # Servidor espera a recibir algo
            
            if not pedido: # Si el pedido no llego
                print("\n>> Cliente desconectado")
                break # El cliente cerró la conexión
            
            print(f"\n>> Se recibe desde el cliente la solicitud: {pedido}") # Se imprime la solicitud del cliente

            try: # Interpretamos la solicitud (que sea JSON)
                solicitud = json.loads(pedido) # Obtenemos la solicitud desde el cliente
            except json.JSONDecodeError:
                conn.send(b"Solicitud no valida")
                continue

            # Revisamos la solicitud
            if (solicitud["accion"] == "LISTAR_ARTICULOS"): # Listar artículos
                articulos = guardarArticulos(rutaJSON) # Guardamos los artículos en un diccionario
                
                print(f"\n>> Se envia al cliente: {articulos}") # Se imprime lo que se envía al cliente
                
                respuesta = json.dumps(articulos).encode("utf-8") # Serializar el JSON
                conn.send(respuesta) # Envía la respuesta al cliente
            elif (solicitud["accion"] == "BUSCAR_ARTICULOS"): # Buscar artículos
                buscar = solicitud["buscar"].lower() # Guardamos el nombre o marca del artículo
                articulos = guardarArticulos(rutaJSON) # Guardamos los artículos en un diccionario
                counter = 0 # Contador de artículos encontrados

                coincidencias = {"articulos": []} # Cremos el JSON con un diccionario vacío

                for articulo in articulos.get("articulos", []): # Buscamos los artículos
                    if ((buscar in articulo["nombre"].lower()) or (buscar in articulo["marca"].lower())):
                        coincidencias["articulos"].append(articulo) # Agregamos el artículo que coindice con la búsqueda
                        counter += 1
                    
                if (counter > 0): # Si se encontró al menos un artículo
                    print(f"\n>> Se envia al cliente: {coincidencias}") # Se imprime lo que se envía al cliente

                    respuesta = json.dumps(coincidencias).encode("utf-8") # Serializar el JSON
                    conn.send(respuesta) # Envía la respuesta al cliente
                else: # Si no se encontro ningún artículo
                    mensaje = {"mensaje": [{"error": "No hay coincidencias"}]} # Se crea el JSON con el mensaje

                    print(f"\n>> Se envia al cliente: {mensaje}") # Se imprime lo que se envía al cliente

                    respuesta = json.dumps(mensaje).encode("utf-8") # Serializar el JSON
                    conn.send(respuesta)
            else:
                conn.send(b"Comando no reconocido")
        except ConnectionResetError:
            print("\n>> El cliente cerró la conexión abruptamente")
            break
    conn.close() # Cerrar la conexión con el cliente