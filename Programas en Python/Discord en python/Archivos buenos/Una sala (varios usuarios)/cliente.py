import socket, struct, threading, json

MULTICAST_GPR, PORT = ("224.1.1.1", 5007) # Dirección multicast + puerto por sala

class ChatCliente:
    def __init__(self, usuario, sala) -> None:
        # Creamos las variables
        self.usuario = usuario
        self.sala = sala

        # Creamos el socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', PORT)) # Se escucha en todas las interfaces de ese puerto

        grupo = socket.inet_aton(MULTICAST_GPR) # Convierte la IP multicast a bytes
        mreq = struct.pack('4sL', grupo, socket.INADDR_ANY) # Se crea la estructura ip_mreq con la dirección del grupo y la IP de la interfaz
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def recibir(self):
        while (True):
            data, addr = self.sock.recvfrom(4096)
            msj = json.loads(data.decode())

            if (msj['sala'] == self.sala):
                print(f"[{msj['user']}]: {msj['content']}")

    def enviar(self):
        while (True):
            texto = input("")

            mensaje = {
                "tipo": "msj",
                "privado": False,
                "user": self.usuario,
                "sala": self.sala,
                "content": texto
            }

            self.sock.sendto(json.dumps(mensaje).encode(), (MULTICAST_GPR, PORT))

    def iniciar(self):
        threading.Thread(target=self.recibir, daemon=True).start()
        self.enviar()

# Ejemplo de uso
if (__name__ == "__main__"):
    print("Antes de unite a una sala, escribe tu nombre de usuario\n")
    usuario = input("Usuario: ")

    cliente = ChatCliente(usuario, "general")
    cliente.iniciar()