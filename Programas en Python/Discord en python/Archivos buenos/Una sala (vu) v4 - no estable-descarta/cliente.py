import socket, struct, threading, json, sys

MULTICAST_GRP, PORT = ("224.1.1.1", 5007)
SERVER_ADDR = ('127.0.0.1', PORT)  # Dirección del servidor

class ChatCliente:
    def __init__(self, usuario: str, sala: str):
        self.usuario = usuario
        self.sala = sala
        self.activo = True

        # Socket de recepción multicast (Windows requiere bind al puerto destino)
        self.sock_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock_recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock_recv.bind(('', PORT))

        grupo = socket.inet_aton(MULTICAST_GRP)
        mreq = struct.pack('4sL', grupo, socket.INADDR_ANY)
        self.sock_recv.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # Socket de envío unicast al servidor
        self.sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Aviso de inicio al servidor
        inicio = {"tipo": "inicio", "user": self.usuario, "sala": self.sala}
        self.sock_send.sendto(json.dumps(inicio).encode(), SERVER_ADDR)

    def recibir(self):
        while self.activo:
            try:
                data, _ = self.sock_recv.recvfrom(4096)
                msj = json.loads(data.decode())
                if msj.get("sala") != self.sala:
                    continue

                if msj["tipo"] == "msj":
                    if msj.get("privado"):
                        print(f"[Privado de {msj['from']}]: {msj['content']}")
                    else:
                        print(f"[{msj['user']}]: {msj['content']}")
                elif msj["tipo"] == "usuarios":
                    print(f"\nUsuarios en sala '{self.sala}': {', '.join(msj['lista'])}\n")
                elif msj["tipo"] == "aviso":
                    print(msj["content"])
            except:
                break

    def enviar(self):
        while self.activo:
            try:
                texto = input("").strip()
                if texto.lower() == "/salir":
                    salir = {"tipo": "salir", "user": self.usuario, "sala": self.sala}
                    self.sock_send.sendto(json.dumps(salir).encode(), SERVER_ADDR)
                    self.activo = False
                    print("Has salido de la sala.")
                    break

                elif texto.startswith("@"):  # Mensaje privado
                    partes = texto.split(" ", 1)
                    if len(partes) < 2:
                        print("Formato: @usuario mensaje")
                        continue
                    destino, contenido = partes
                    destino = destino[1:]
                    mensaje = {
                        "tipo": "msj",
                        "privado": True,
                        "from": self.usuario,
                        "to": destino,
                        "content": contenido,
                        "sala": self.sala
                    }
                    self.sock_send.sendto(json.dumps(mensaje).encode(), SERVER_ADDR)
                    print(f"[Tú -> {destino}]: {contenido}")
                    continue

                # Mensaje público
                mensaje = {
                    "tipo": "msj",
                    "privado": False,
                    "user": self.usuario,
                    "sala": self.sala,
                    "content": texto
                }
                self.sock_send.sendto(json.dumps(mensaje).encode(), SERVER_ADDR)

            except KeyboardInterrupt:
                salir = {"tipo": "salir", "user": self.usuario, "sala": self.sala}
                self.sock_send.sendto(json.dumps(salir).encode(), SERVER_ADDR)
                self.activo = False
                sys.exit(0)

    def iniciar(self):
        threading.Thread(target=self.recibir, daemon=True).start()
        self.enviar()


if __name__ == "__main__":
    print("Antes de unirte a la sala, escribe tu nombre de usuario\n")
    usuario = input("Usuario: ")
    cliente = ChatCliente(usuario, "general")
    cliente.iniciar()