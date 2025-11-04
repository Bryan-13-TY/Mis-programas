import socket, threading, json, sys, sounddevice as sd, wavio
from datetime import datetime
from pathlib import Path

SERVER_IP, SERVER_PORT = "127.0.0.1", 5007  # IP y puerto del servidor

# Colores ANSI
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
ORANGE = "\033[33m"
RESET = "\033[0m"

class Cliente:
    def __init__(self, usuario: str, sala: str) -> None:
        """
        Método principal de la clase.

        Parameters
        ----------
        usuario : str
            Nombre de usuario del cliente.
        sala : srt
            Nombre de la sala en la que se encuentra el cliente.
        """
        self.usuario = usuario
        self.sala = sala
        self.activo = True

        # Se crea el socket UDP para enviar y recibir mensajes
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Se crea un socket UDP
        self.sock.bind(('', 0))  # Puerto aleatorio para recibir mensajes

        # Avisar al servidor que un usuario entro a la sala
        inicio = {"tipo": "inicio",
                  "user": self.usuario,
                  "sala": self.sala}
        
        self.sock.sendto(json.dumps(inicio).encode(), (SERVER_IP, SERVER_PORT))

    def grabar_audio(self) -> None:
        """Método para grabar un audio, reproducirlo y posteriormente guardarlo."""
        # Se construye la ruta donde se guardara la grabación
        carpeta_script = Path(__file__).parent
        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        ruta_grabacion = carpeta_script/f"{self.sala}"/f"grabacion_{self.usuario}_{fecha}.wav"
        ruta_grabacion.parent.mkdir(parents=True, exist_ok=True) # Se crea la carpeta si no existe

        # Parámetros
        duracion, frecuencia = (5, 44100) # (segundos, Hz 'calidad estándar de audio')

        print("[Sistema] Grabando audio...")

        audio = sd.rec(int(duracion * frecuencia), samplerate=frecuencia, channels=2)

        sd.wait() # Esperar a que termine la grabación
        print("[Sistema] Grabación completa")
        wavio.write(str(ruta_grabacion), audio, frecuencia, sampwidth=2) # Guardar la grabación

        #print(f"Audio guardado como '{ruta_grabacion}")
        print("[Sistema] Reproduciendo grabación...")

        sd.play(audio, frecuencia) # Reproducir la grabación
        sd.wait() # Esperar a que termine la reproducción

        print("[Sistema] Reproducción terminada")

    def recibir(self) -> None:
        """Método para recibir mensajes enviados desde el servidor."""
        while (self.activo): # Mientras el usuario siga en una sala
            try:
                data, _ = self.sock.recvfrom(4096)
                mensaje = json.loads(data.decode())
                sala_mensaje = mensaje.get("sala", self.sala)
                tipo = mensaje["tipo"]

                if (sala_mensaje != self.sala):
                    # Si el mensaje no se envía a la sala actual se ignoras
                    continue

                if (tipo == "msj"): # Si es un mensaje
                    if (mensaje.get("privado")): # Si es un mensaje privado
                        print(f"{YELLOW}[Privado de {mensaje['from']}]{RESET}: {mensaje['content']}")
                    else: # Si es un mensaje público
                        print(f"{BLUE}[{mensaje['user']}]{RESET}: {mensaje['content']}")
                
                if (tipo == "aviso"): # Si es un avio
                    print(mensaje["content"])
                
                if (tipo == "usuarios"): # Si es la lista de usuarios conectados
                    print(f"\nUsuarios en sala {MAGENTA}'{self.sala}'{RESET}: {MAGENTA}{', '.join(mensaje['lista'])}{RESET}\n")
            except:
                break

    def sticker(self, nombre_sticker: str) -> str:
        """
        Método para seleccionar el sticker.
        
        Parameters
        ----------
        nombre_sticker : str
            Nombre del sticker seleccioando.
        """
        match (nombre_sticker):
            case 'shrek':
                sticker_enviar = """
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
                sticker_enviar = """
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
                sticker_enviar = """
 / \\__
(    @\\___
 /         O
/   (_____/
/_____/   U
"""
            case 'cat':
                sticker_enviar = """
 /\\_/\\
( o.o )
 > ^ <
"""
            case 'heart':
                sticker_enviar = """
  **     **
 *****  *****
**************
 ************
  **********
    ******
      **
"""
            case 'rocket':
                sticker_enviar = """
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
                sticker_enviar = """
 (\\_/)
 ( •_•)
 / >🍪
"""
            case 'owl':
                sticker_enviar = """
 ,_,  
(O,O) 
(   ) 
 " "
"""
            case 'dinosaur':
                sticker_enviar = """
           __
          / _)
   .-^^^-/ /
__/       /
<__.|_|-|_|
"""
            case _:
                return ""
        
        return sticker_enviar
            
    def enviar(self) -> None:
        """Método para enviar mensajes al servidor."""
        while (self.activo): # Mientras el usuario siga en una sala
            try:
                texto_entrada = input("").strip()
                
                if (texto_entrada.lower() == "/salir"): # Si quiere salir de la sala
                    salir = {"tipo": "salir",
                             "user": self.usuario,
                             "sala": self.sala}
                    
                    self.sock.sendto(json.dumps(salir).encode(), (SERVER_IP, SERVER_PORT))
                    self.activo = False
                    
                    print("[Sistema] Has salido de la sala")
                    break
                elif (texto_entrada.lower() == "/audio"): # Si quiere grabar un audio
                    audio = {"tipo": "audio",
                             "user": self.usuario,
                             "sala": self.sala}
                    
                    self.grabar_audio()
                    self.sock.sendto(json.dumps(audio).encode(), (SERVER_IP, SERVER_PORT))
                elif ((texto_entrada.lower()).split(" ", 1)[0] == "/sticker"): # Si es un sticker público
                    partes = texto_entrada.split(" ", 1)

                    if (len(partes) < 2): # Si el formato no es el correcto
                        print("[Sistema] Formato: /sticker nombre_sticker")
                        continue

                    _, nombre_sticker = partes

                    sticker = self.sticker(nombre_sticker)

                    if (not sticker):
                        print("[Sistema] El sticker no existe")
                        continue

                    mensaje = {"tipo": "msj",
                               "privado": False,
                               "user": self.usuario,
                               "sala": self.sala,
                               "content": sticker}
                    
                    self.sock.sendto(json.dumps(mensaje).encode(), (SERVER_IP, SERVER_PORT))
                elif (texto_entrada.startswith("@")): # Si es un mensaje privado
                    partes = texto_entrada.split(" ", 1)
                    
                    if (len(partes) < 2): # Si el formato no es el correcto
                        print("[Sistema] Formato: @usuario mensaje")
                        continue

                    destinatario, contenido = partes
                    destinatario = destinatario[1:] # Quitar '@'
                    mensaje = {"tipo": "msj",
                               "privado": True,
                               "from": self.usuario,
                               "to": destinatario,
                               "content": contenido,
                               "sala": self.sala}
                    
                    self.sock.sendto(json.dumps(mensaje).encode(), (SERVER_IP, SERVER_PORT))
                    
                    print(f"{ORANGE}[Tú -> {destinatario}]{RESET}: {contenido}")
                    continue
                else: # Si es un mensaje público
                    mensaje = {"tipo": "msj",
                               "privado": False,
                               "user": self.usuario,
                               "sala": self.sala,
                               "content": texto_entrada}
                    
                    self.sock.sendto(json.dumps(mensaje).encode(), (SERVER_IP, SERVER_PORT))
            except KeyboardInterrupt: # El usuario presiona Ctrl + C (salir de la sala)
                salir = {"tipo": "salir",
                         "user": self.usuario,
                         "sala": self.sala}
                
                self.sock.sendto(json.dumps(salir).encode(), (SERVER_IP, SERVER_PORT))
                self.activo = False
                
                sys.exit(0)

    def iniciar(self) -> None:
        """Método para inicializar los hilos. Un hilo para recibir mensajes en segundo plano y uno principal para enviar."""
        threading.Thread(target=self.recibir, daemon=True).start()
        self.enviar()

def main() -> None:
    usuario = input("Antes de unirte a la sala, escribe tu nombre de usuario:\nUsuario: ")
    cliente = Cliente(usuario, "general")
    cliente.iniciar()

if (__name__ == "__main__"):
    main()