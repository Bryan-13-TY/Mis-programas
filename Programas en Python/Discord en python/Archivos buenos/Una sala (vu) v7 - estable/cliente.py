import socket, threading, json, sys, sounddevice as sd, wavio
from datetime import datetime
from pathlib import Path

SERVER_IP, SERVER_PORT = "127.0.0.1", 5007  # IP y puerto del servidor

YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
ORANGE = "\033[33m"
RESET = "\033[0m"

class ChatCliente:
    def __init__(self, usuario: str, sala: str) -> None:
        self.usuario = usuario
        self.sala = sala
        self.activo = True

        # Socket UDP para enviar y recibir
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', 0))  # Puerto aleatorio para recibir mensajes

        # Avisar al servidor que entra el usuario
        inicio = {"tipo": "inicio", "user": self.usuario, "sala": self.sala}
        self.sock.sendto(json.dumps(inicio).encode(), (SERVER_IP, SERVER_PORT))

    def grabar_audio(self) -> None:
        """
        Métodod que graba audio, lo reproduce y despupes lo guarda.
        """
        # Se contruye la ruta donde se guarda la grabación
        carpeta_script = Path(__file__).parent
        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        ruta_grabacion = carpeta_script/f"{self.sala}"/f"grabacion_{self.usuario}_{fecha}.wav"

        # Si la carpeta no existe se crea
        ruta_grabacion.parent.mkdir(parents=True, exist_ok=True)

        # Parámetros
        duracion, frecuencia = (10, 44100) # (segundos, Hz 'calidad estándar de audio')

        print("Grabando audio...")

        audio = sd.rec(int(duracion * frecuencia), samplerate=frecuencia, channels=2)

        sd.wait() # Esperar a que termine la grabación
        print("Grabación completa")

        # Guardar la grabación
        wavio.write(str(ruta_grabacion), audio, frecuencia, sampwidth=2)

        #print(f"Audio guardado como '{ruta_grabacion}")
        print("Reproduciendo grabación...")

        sd.play(audio, frecuencia)
        sd.wait()

        print("Reproducción terminada")

    def recibir(self) -> None:
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
                        print(f"{YELLOW}[Privado de {msj['from']}]{RESET}: {msj['content']}")
                    else: # Si es un mensaje público
                        print(f"{BLUE}[{msj['user']}]{RESET}: {msj['content']}")
                elif (msj["tipo"] == "aviso"): # Si es un avio
                    print(msj["content"])
                elif (msj["tipo"] == "usuarios"): # Si es la lista de usuario en la sala
                    print(f"\nUsuarios en sala {MAGENTA}'{self.sala}'{RESET}: {MAGENTA}{', '.join(msj['lista'])}{RESET}\n")
            except:
                break

    def enviar(self) -> None:
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
                elif (texto.lower() == "/audio"): # Si el usuario quiere grabar un audio
                    audio = {"tipo": "audio", "user": self.usuario, "sala": self.sala}
                    
                    self.grabar_audio()
                    self.sock.sendto(json.dumps(audio).encode(), (SERVER_IP, SERVER_PORT))
                elif ((texto.lower()).split(" ", 1)[0] == "/sticker"):
                    partes = texto.split(" ", 1)

                    if (len(partes) < 2):
                        print("Formato: /sticker sticker")
                        continue

                    _, contenido = partes

                    match (contenido):
                        case 'shrek':
                            sticker = """
⡴⠑⡄⠀⠀⠀⠀⠀⠀⠀ ⣀⣀⣤⣤⣤⣀⡀
⠸⡇⠀⠿⡀⠀⠀⠀⣀⡴⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀
⠀⠀⠀⠀⠑⢄⣠⠾⠁⣀⣄⡈⠙⣿⣿⣿⣿⣿⣿⣿⣿⣆
⠀⠀⠀⠀⢀⡀⠁⠀⠀⠈⠙⠛⠂⠈⣿⣿⣿⣿⣿⠿⡿⢿⣆
⠀⠀⠀⢀⡾⣁⣀⠀⠴⠂⠙⣗⡀⠀⢻⣿⣿⠭⢤⣴⣦⣤⣹⠀⠀⠀⢀⢴⣶⣆
⠀⠀⢀⣾⣿⣿⣿⣷⣮⣽⣾⣿⣥⣴⣿⣿⡿⢂⠔⢚⡿⢿⣿⣦⣴⣾⠸⣼⡿
⠀⢀⡞⠁⠙⠻⠿⠟⠉⠀⠛⢹⣿⣿⣿⣿⣿⣌⢤⣼⣿⣾⣿⡟⠉
⠀⣾⣷⣶⠇⠀⠀⣤⣄⣀⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⠀⠉⠈⠉⠀⠀⢦⡈⢻⣿⣿⣿⣶⣶⣶⣶⣤⣽⡹⣿⣿⣿⣿⡇
⠀⠀⠀⠀⠀⠀⠀⠉⠲⣽⡻⢿⣿⣿⣿⣿⣿⣿⣷⣜⣿⣿⣿⡇
   ⠀⠀⠀⠀⠀⢸⣿⣿⣷⣶⣮⣭⣽⣿⣿⣿⣿⣿⣿⣿⠇
⠀⠀⠀⠀⠀⠀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇
⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
"""
                        case 'heisenberg':
                            sticker = """
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠆⠜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠿⠿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡏⠁⠀⠀⠀⠀⠀⣀⣠⣤⣤⣶⣶⣶⣶⣶⣦⣤⡄⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡧⠇⢀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣮⣭⣿⡻⣽⣒⠀⣤⣜⣭⠐⢐⣒⠢⢰⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣿⣿⣿⣿⣿⣿⡟⣾⣿⠂⢈⢿⣷⣞⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣷⣶⣾⡿⠿⣿⠗⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠻⠋⠉⠑⠀⠀⢘⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⢹⣿⣿⡇⢀⣶⣶⠴⠶⠀⠀⢽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⢸⣿⣿⠀⠀⠣⠀⠀⠀⠀⠀⡟⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡿⠟⠋⠀⠀⠀⠀⠹⣿⣧⣀⠀⠀⠀⠀⡀⣴⠁⢘⡙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⠗⠂⠄⠀⣴⡟⠀⠀⡃⠀⠉⠉⠟⡿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢷⠾⠛⠂⢹⠀⠀⠀⢡⠀⠀⠀⠀⠀⠙⠛⠿⢿⣿⣿⣿⣿⣿⣿
"""
                        case 'dog':
                            sticker = """
 / \\__
(    @\\___
 /         O
/   (_____/
/_____/   U
"""
                        case 'cat':
                            sticker = """
 /\\_/\\
( o.o )
 > ^ <
"""
                        case 'heart':
                            sticker = """
  **     **
 *****  *****
**************
 ************
  **********
    ******
      **
"""
                        case 'rocket':
                            sticker = """
    ^
   /^\\
  /___\\
  |= |=
  |.-.|
  |'-'|
  |   |
 /|_|_|\\
   / \\
  /___\\
"""
                        case 'rabbit':
                            sticker = """
 (\\_/)
 ( •_•)
 / >🍪
"""
                        case 'owl':
                            sticker = """
 ,_,  
(O,O) 
(   ) 
 " "
"""
                        case 'dinosaur':
                            sticker = """
           __
          / _)
   .-^^^-/ /
__/       /
<__.|_|-|_|
"""
                        case _:
                            print("El sticker no existe")
                            continue

                    mensaje = {"tipo": "msj", "privado": False, "user": self.usuario,
                            "sala": self.sala, "content": sticker}
                    
                    self.sock.sendto(json.dumps(mensaje).encode(), (SERVER_IP, SERVER_PORT))
                # Mensaje privado: @usuario mensaje
                elif (texto.startswith("@")): # Si el usuaario quiere enviar un mensaje privado
                    partes = texto.split(" ", 1)
                    
                    if (len(partes) < 2): # Si el formato no es el correcto
                        print("Formato: @usuario mensaje")
                        continue

                    destino, contenido = partes
                    destino = destino[1:] # Quitar '@'
                    mensaje = {"tipo": "msj", "privado": True, "from": self.usuario,
                               "to": destino, "content": contenido, "sala": self.sala}
                    
                    self.sock.sendto(json.dumps(mensaje).encode(), (SERVER_IP, SERVER_PORT))
                    
                    print(f"{ORANGE}[Tú -> {destino}]{RESET}: {contenido}")
                    continue
                # Mensaje público
                else:
                    mensaje = {"tipo": "msj", "privado": False, "user": self.usuario,
                            "sala": self.sala, "content": texto}
                    
                    self.sock.sendto(json.dumps(mensaje).encode(), (SERVER_IP, SERVER_PORT))
            except KeyboardInterrupt: # El usuario presiona Ctrl + C (salir de la sala)
                salir = {"tipo": "salir", "user": self.usuario, "sala": self.sala}
                
                self.sock.sendto(json.dumps(salir).encode(), (SERVER_IP, SERVER_PORT))
                self.activo = False
                
                sys.exit(0)

    def iniciar(self) -> None:
        """
        Método para inicializar los hilos. Un hilo para recibir mensajes en segundo plano y uno principal para enviar.
        """
        threading.Thread(target=self.recibir, daemon=True).start()
        self.enviar()

def main() -> None:
    usuario = input("Antes de unirte a la sala, escribe tu nombre de usuario:\nUsuario: ")
    cliente = ChatCliente(usuario, "general")
    cliente.iniciar()

if (__name__ == "__main__"):
    main()