import socket, struct, threading, json

MULTICAST_GRP, PORT = ("224.1.1.1", 5007) # Grupo multicast y el puerto
# Las direcciones 224.0.0.0 - 239.255.255.255 son reservadas para multicast

class ChatCliente: # Representa a un cliente del chat qu se conecta
    def __init__(self, usuario: str, sala: str) -> None:
        # Creamos los atributos de objeto
        self.usuario = usuario
        self.sala = sala

        # Creamos el socket (atributo de objeto)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # Creación del socket UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Permite que varios sockets se vinculen al mismo puerto
        self.sock.bind(('', PORT)) # Asocia el socket al puerto 5007 en todas las interfaces de red

        # Unirse al grupo multicast
        grupo = socket.inet_aton(MULTICAST_GRP) # Convierte la IP multicast a formato binario
        mreq = struct.pack('4sL', grupo, socket.INADDR_ANY) # Grupo multicast (4 bytes), cualquier interfaz disponible (entero largo)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq) # Hace que el socket se una al grupo multicast, recibiendo los mensajes enviados al grupo 224.1.1.1

    def recibir(self):
        """
        Método para recibir mensajes de cualquier usuario.
        """
        while (True):
            data, addr = self.sock.recvfrom(4096) # Espera a recibir un datagrama UDP (1024 bytes)
            msj = json.loads(data.decode()) # Decodifica el mensaje recibido

            if (msj['sala'] == self.sala): # Muestra los mensajes que pertenecen a la misma sala del cliente
                print(f"[{msj['user']}]: {msj['content']}")

    def enviar(self):
        """
        Métodod para enviar mensajes de cualquier usuario.
        """
        while (True):
            texto = input("")

            mensaje = {
                "tipo": "msj",
                "privado": False,
                "user": self.usuario,
                "sala": self.sala,
                "content": texto
            }

            self.sock.sendto(json.dumps(mensaje).encode(), (MULTICAST_GRP, PORT)) # Envía el mensaje al grupo multicast

    def iniciar(self):
        """
        Métodod que crea un hilo en segundo plano.
        """
        threading.Thread(target=self.recibir, daemon=True).start()
        self.enviar()

# Ejemplo de uso
if (__name__ == "__main__"):
    print("Antes de unite a una sala, escribe tu nombre de usuario\n")
    usuario = input("Usuario: ")

    cliente = ChatCliente(usuario, "general")
    cliente.iniciar() # Enlaza los hilos de envío y recepción