import socket, threading, json, sys

SERVER_IP, SERVER_PORT = "127.0.0.1", 5007  # IP y puerto del servidor

class ChatCliente:
    def __init__(self, usuario: str, sala: str):
        self.usuario = usuario
        self.sala = sala
        self.activo = True

        # Socket UDP para enviar y recibir
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', 0))  # Puerto aleatorio para recibir mensajes

        # Avisar al servidor que entra el usuario
        inicio = {"tipo": "inicio", "user": self.usuario, "sala": self.sala}
        self.sock.sendto(json.dumps(inicio).encode(), (SERVER_IP, SERVER_PORT))

    def recibir(self):
        """
        Método para recibir mensajes enviados solo a ese cliente.
        """
        while (self.activo):
            try:
                data, _ = self.sock.recvfrom(4096)
                msj = json.loads(data.decode())
                sala_msg = msj.get("sala", self.sala)

                if (sala_msg != self.sala): # Si el mensaje no pertenece a la sala lo ignora
                    continue

                if (msj["tipo"] == "msj"): # Si es un mensaje
                    if (msj.get("privado")): # Si es un mensaje privado
                        print(f"[Privado de {msj['from']}]: {msj['content']}")
                    else: # Si es un mensaje público
                        print(f"[{msj['user']}]: {msj['content']}")
                elif (msj["tipo"] == "aviso"): # Si es un avio
                    print(msj["content"])
                elif (msj["tipo"] == "usuarios"): # Si es la lista de usuario en la sala
                    print(f"\nUsuarios en sala '{self.sala}': {', '.join(msj['lista'])}\n")
            except:
                break

    def enviar(self):
        """
        Método para enviar mensajes al servidor.
        """
        while (self.activo):
            try:
                texto = input("").strip()
                
                if (texto.lower() == "/salir"): # Si el usuario quiere abandonar la sala
                    salir = {"tipo": "salir", "user": self.usuario, "sala": self.sala}
                    
                    self.sock.sendto(json.dumps(salir).encode(), (SERVER_IP, SERVER_PORT))
                    self.activo = False
                    
                    print("Has salido de la sala.")
                    break
                # Mensaje privado: @usuario mensaje
                if (texto.startswith("@")): # Si el usuaario quiere enviar un mensaje privado
                    partes = texto.split(" ", 1)
                    
                    if (len(partes) < 2): # Si el formato no es el correcto
                        print("Formato: @usuario mensaje")
                        continue

                    destino, contenido = partes
                    destino = destino[1:] # Quitar '@'
                    mensaje = {"tipo": "msj", "privado": True, "from": self.usuario,
                               "to": destino, "content": contenido, "sala": self.sala}
                    
                    self.sock.sendto(json.dumps(mensaje).encode(), (SERVER_IP, SERVER_PORT))
                    
                    print(f"[Tú -> {destino}]: {contenido}")
                    continue
                # Mensaje público
                mensaje = {"tipo": "msj", "privado": False, "user": self.usuario,
                           "sala": self.sala, "content": texto}
                
                self.sock.sendto(json.dumps(mensaje).encode(), (SERVER_IP, SERVER_PORT))
            except KeyboardInterrupt: # El usuario presiona Ctrl + C (salir de la sala)
                salir = {"tipo": "salir", "user": self.usuario, "sala": self.sala}
                
                self.sock.sendto(json.dumps(salir).encode(), (SERVER_IP, SERVER_PORT))
                self.activo = False
                
                sys.exit(0)

    def iniciar(self):
        """
        Método para inicializar los hilos. Un hilo para recibir mensajes en segundo plano y uno principal para enviar.
        """
        threading.Thread(target=self.recibir, daemon=True).start()
        self.enviar()

if (__name__ == "__main__"):
    usuario = input("Antes de unirte a la sala, escribe tu nombre de usuario:\nUsuario: ")
    cliente = ChatCliente(usuario, "general")
    cliente.iniciar()