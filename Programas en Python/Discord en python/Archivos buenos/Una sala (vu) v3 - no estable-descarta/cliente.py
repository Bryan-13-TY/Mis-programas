import socket, struct, threading, json, sys

MULTICAST_GRP, PORT = ("224.1.1.1", 5007) # Grupo multicast y el puerto
SERVER_ADDR = (MULTICAST_GRP, PORT)
# Las direcciones 224.0.0.0 - 239.255.255.255 son reservadas para multicast

class ChatCliente: # Representa a un cliente del chat qu se conecta
    def __init__(self, usuario: str, sala: str) -> None:
        # Creamos los atributos de objeto
        self.usuario = usuario
        self.sala = sala
        self.activo = True

        # Creamos el socket UDP  multicast (atributo de objeto)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # Creación del socket UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Permite que varios sockets se vinculen al mismo puerto
        self.sock.bind(('', PORT)) # Asocia el socket al puerto 5007 en todas las interfaces de red

        # Unirse al grupo multicast
        grupo = socket.inet_aton(MULTICAST_GRP) # Convierte la IP multicast a formato binario
        mreq = struct.pack('4sL', grupo, socket.INADDR_ANY) # Grupo multicast (4 bytes), cualquier interfaz disponible (entero largo)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq) # Hace que el socket se una al grupo multicast, recibiendo los mensajes enviados al grupo 224.1.1.1

        # Enviar aviso de inicio al servidor
        inicio = {"tipo": "inicio", "user": self.usuario, "sala": self.sala}
        self.sock.sendto(json.dumps(inicio).encode(), SERVER_ADDR)

    def recibir(self):
        """
        Método para recibir mensajes de cualquier usuario.
        """
        while (self.activo):
            try:
                data, addr = self.sock.recvfrom(4096) # Espera a recibir un datagrama UDP (4096 bytes)
                msj = json.loads(data.decode()) # Decodifica el mensaje recibido

                if (msj.get("sala") != self.sala):
                    continue

                # Mostrar mensajes según su tipo
                if (msj["tipo"] == "msj"):
                    if (msj.get("privado")):
                        print(f"[Privado de {msj['from']}]: {msj['content']}")
                    else:
                        print(f"[{msj['user']}]: {msj['content']}")
                elif (msj["tipo"] == "usuarios"):
                    print(f"\nUsuarios en sala '{self.sala}': {', '.join(msj['lista'])}\n")
                elif (msj["tipo"] == "aviso"):
                    print(msj["content"])
            except:
                break

    def enviar(self):
        """
        Métodod para enviar mensajes de cualquier usuario.
        """
        while (self.activo):
            try:
                texto = input("").strip()

                if (texto.lower() == "/salir"):
                    salir = {"tipo": "salir", "user": self.usuario, "sala": self.sala}
                    self.sock.sendto(json.dumps(salir).encode(), SERVER_ADDR)
                    self.activo = False
                    print("Has salido de la sala.")
                    break
                # Mensaje privado -> formato: @usuario mensaje
                elif (texto.startswith("@")):
                    partes = texto.split(" ", 1)

                    if (len(partes) < 2):
                        print("Formato: @usuario mensaje")
                        continue

                    destino, contenido = partes
                    destino = destino[1:] # Quitar '@'
                    # Mensaje nor
                    mensaje = {
                        "tipo": "msj",
                        "privado": True,
                        "from": self.usuario,
                        "to": destino,
                        "content": contenido,
                        "sala": self.sala
                    }

                    self.sock.sendto(json.dumps(mensaje).encode(), SERVER_ADDR) # Envía el mensaje al grupo multicast
                    
                    print(f"[Tú -> {destino}]: {contenido}")
                    continue

                # Mensaje normal (público)
                mensaje = {
                    "tipo": "msj",
                    "privado": False,
                    "user": self.usuario,
                    "sala": self.sala,
                    "content": texto
                }

                self.sock.sendto(json.dumps(mensaje).encode(), SERVER_ADDR)

            except KeyboardInterrupt:
                # Enviar aviso al salir con Ctrl+C
                salir = {"tipo": "salir", "user": self.usuario, "sala": self.sala}
                self.sock.sendto(json.dumps(salir).encode(), SERVER_ADDR)
                self.activo = False
                sys.exit(0)

    def iniciar(self):
        """
        Método que crea un hilo en segundo plano.
        """
        threading.Thread(target=self.recibir, daemon=True).start()
        self.enviar()

# Ejemplo de uso
if (__name__ == "__main__"):
    print("Antes de unite a una sala, escribe tu nombre de usuario\n")
    usuario = input("Usuario: ")

    cliente = ChatCliente(usuario, "general")
    cliente.iniciar() # Enlaza los hilos de envío y recepción