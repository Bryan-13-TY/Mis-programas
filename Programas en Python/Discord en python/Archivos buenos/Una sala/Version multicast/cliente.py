import socket, struct, threading, json, sys

MULTICAST_GRP, PORT = ("224.1.1.1", 5007) # Grupo multicast y el puerto
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
        self.sock.sendto(json.dumps(inicio).encode(), (MULTICAST_GRP, PORT))

    def recibir(self):
        """
        Método para recibir mensajes de cualquier usuario.
        """
        while (self.activo):
            try:
                data, addr = self.sock.recvfrom(4096) # Espera a recibir un datagrama UDP (4096 bytes)
                msj = json.loads(data.decode()) # Decodifica el mensaje recibido

                if (msj["sala"] != self.sala):
                    continue

                # Mostrar mensajes según su tipo
                if (msj["tipo"] == "msj"):
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
                    self.sock.sendto(json.dumps(salir).encode(), (MULTICAST_GRP, PORT))
                    self.activo = False
                    print("Has salido de la sala.")
                    break

                # Mensaje normal a la sala
                mensaje = {
                "tipo": "msj",
                "privado": False,
                "user": self.usuario,
                "sala": self.sala,
                "content": texto
                }

                self.sock.sendto(json.dumps(mensaje).encode(), (MULTICAST_GRP, PORT)) # Envía el mensaje al grupo multicast
            except KeyboardInterrupt:
                # Enviar aviso al salir con Ctrl+C
                salir = {"tipo": "salir", "user": self.usuario, "sala": self.sala}
                self.sock.sendto(json.dumps(salir).encode(), (MULTICAST_GRP, PORT))
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