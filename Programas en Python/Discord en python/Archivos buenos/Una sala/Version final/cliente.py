import socket, threading, json, sys, shutil, time
from pathlib import Path
from audio import Audio

# Colores ANSI
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
ORANGE = "\033[33m"
RESET = "\033[0m"

SERVER_IP, SERVER_PORT = "127.0.0.1", 5007  # IP y puerto del servidor

class Cliente:
    def __init__(self, usuario: str, sala: str) -> None:
        """
        Constructor de la clase.

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
        self.audio = Audio() # Objeto de tipo audio

        # Se crea el socket UDP para enviar y recibir mensajes
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Se crea un socket UDP
        self.sock.bind(('', 0))  # Puerto aleatorio para recibir mensajes
        
        self.carpeta_script = Path(__file__).parent
        self.carpeta_sala = self.carpeta_script / f"{self.sala}" # Carpeta de la sala
        self.carpeta_sala.mkdir(parents=True, exist_ok=True)
        self.carpeta_usuario = self.carpeta_sala / f"{self.usuario}" # Carpeta del usuario
        self.carpeta_usuario.mkdir(parents=True, exist_ok=True)

        # Avisar al servidor que un usuario entro a la sala
        inicio = {"tipo": "inicio",
                  "user": self.usuario,
                  "sala": self.sala}
        
        self.sock.sendto(json.dumps(inicio).encode(), (SERVER_IP, SERVER_PORT))

    def sticker(self, nombre_sticker: str) -> str:
        """
        Método para seleccionar el sticker.
        
        Parameters
        ----------
        nombre_sticker : str
            Nombre del sticker seleccioando.
        
        Returns
        -------
        str
            Sticker seleccionado por el usuario.
        """
        match (nombre_sticker):
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
                return ""
        
        return sticker

    def recibir_mensaje(self) -> None:
        """Método para recibir mensajes enviados desde el servidor."""
        while (self.activo): # Mientras el usuario siga en una sala
            try:
                data, _ = self.sock.recvfrom(4096)
                mensaje = json.loads(data.decode())
                sala_mensaje = mensaje.get("sala", self.sala)
                tipo = mensaje.get("tipo")

                if (sala_mensaje != self.sala):
                    # Si el mensaje no se envía a la sala actual se ignoras
                    continue

                if (tipo == "msj"):
                    if (mensaje.get("privado")):
                        print(f"{YELLOW}[Privado de {mensaje['from']}]{RESET}: {mensaje['content']}")
                    else:
                        print(f"{BLUE}[{mensaje['user']}]{RESET}: {mensaje['content']}")
                
                if (tipo == "aviso"):
                    print(mensaje["content"])

                if (tipo == "audio"):
                    print(f"{YELLOW}[Privado de {mensaje['from']}]{RESET}: {mensaje['content']}")
                
                if (tipo == "usuarios"):
                    print(f"Usuarios en sala {MAGENTA}'{self.sala}'{RESET}: {MAGENTA}{', '.join(mensaje['lista'])}{RESET}")
            except:
                break
            
    def enviar_mensaje(self) -> None:
        """Método para enviar mensajes al servidor."""
        while (self.activo):
            try:
                texto = input("").strip()
                
                if (texto.lower() == "/salir"):
                    salir = {"tipo": "salir",
                             "user": self.usuario,
                             "sala": self.sala}
                    
                    self.sock.sendto(json.dumps(salir).encode(), (SERVER_IP, SERVER_PORT))
                    
                    if (self.carpeta_usuario.exists()): # Si existe se borra
                        time.sleep(0.5)  # medio segundo de espera
                        shutil.rmtree(self.carpeta_usuario) # Se borra la carpeta del usuario
                    
                    self.activo = False
                    
                    print(">> [system] Has salido de la sala")
                    break

                elif (texto.lower() == "/audio"):
                    audio = {"tipo": "audio",
                             "privado": False,
                             "user": self.usuario,
                             "sala": self.sala}
                    
                    nombre_audio = self.audio.grabar_audio(audio, self.carpeta_script, self.sala, self.usuario)
                    audio.update({"nombre": nombre_audio})
                    self.sock.sendto(json.dumps(audio).encode(), (SERVER_IP, SERVER_PORT))
                
                elif (texto.lower().startswith("/sticker")):
                    partes = texto.split(" ", 1)

                    if (len(partes) < 2): # Si el formato no es el correcto
                        print(">> [system] Formato: /sticker nombre_sticker")
                        continue

                    _, nombre_sticker = partes # Se obtiene el nombre del sticker
                    sticker = self.sticker(nombre_sticker) # Se obtiene el sticker

                    if (not sticker): # Si el sticker no existe
                        print(">> [system] El sticker no existe")
                        continue

                    mensaje = {"tipo": "msj",
                               "privado": False,
                               "user": self.usuario,
                               "sala": self.sala,
                               "content": sticker}
                    
                    self.sock.sendto(json.dumps(mensaje).encode(), (SERVER_IP, SERVER_PORT))

                elif (texto.lower().startswith("/reproducir")):
                    partes = texto.split(" ", 1)

                    if (len(partes) < 2): # Si el formato no es el correcto
                        print(">> [system] Formato: /reproducir nombre_archivo")
                        continue

                    _, nombre_archivo = partes # Se obtiene el nombre del audio grabado
                    ruta_audio = self.audio.buscar_audio(self.carpeta_sala, self.carpeta_usuario, self.usuario, nombre_archivo)

                    if (ruta_audio): # Si existe el audio
                        self.audio.reproducir_audio(ruta_audio, nombre_archivo)
                    else:
                        print(">> [system] El audio no existe")

                elif (texto.startswith("@")): # Si es un mensaje privado
                    partes = texto.split(" ", 1)
                    
                    if (len(partes) < 2): # Si el formato no es el correcto
                        print(">> [system] Formato: @usuario mensaje")
                        continue

                    if (partes[1].startswith("/sticker")):
                        partes2 = partes[1].split(" ")

                        if (len(partes2) < 2): # Si el formato no es correcto
                            print("[Sistema] Formato: /sticker nombre_sticker")
                            continue

                        _, nombre_sticker = partes2
                        sticker = self.sticker(nombre_sticker)

                        if (not sticker): # Si el sticker no existe
                            print(">> [system] El sticker no existe")
                            continue

                        destinatario, _ = partes
                        destinatario = destinatario[1:] # Quitar '@'
                        mensaje = {"tipo": "msj",
                                   "privado": True,
                                   "from": self.usuario,
                                   "to": destinatario,
                                   "content": sticker,
                                   "sala": self.sala}
                        
                        self.sock.sendto(json.dumps(mensaje).encode(), (SERVER_IP, SERVER_PORT))
                    
                        print(f"{ORANGE}[Tú -> {destinatario}]{RESET}: {sticker}")
                        continue
                    
                    elif (partes[1] == "/audio"):
                        destinatario, _ = partes
                        destinatario = destinatario[1:] # Quitar '@'

                        audio = {"tipo": "audio",
                                 "privado": True,
                                 "from": self.usuario,
                                 "to": destinatario,
                                 "sala": self.sala}
                        
                        nombre_audio = self.audio.grabar_audio(audio, self.carpeta_script, self.sala, self.usuario)
                        audio.update({"content": f"te ha enviado el audio '{nombre_audio}'"})
                        self.sock.sendto(json.dumps(audio).encode(), (SERVER_IP, SERVER_PORT))

                        print(f"{ORANGE}[Tú -> {destinatario}]{RESET}: has enviado el audio '{nombre_audio}'")
                        continue

                    else:
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
                               "content": texto}
                    
                    self.sock.sendto(json.dumps(mensaje).encode(), (SERVER_IP, SERVER_PORT))
            except KeyboardInterrupt: # El usuario presiona Ctrl + C (salir de la sala)
                salir = {"tipo": "salir",
                         "user": self.usuario,
                         "sala": self.sala}
                
                self.sock.sendto(json.dumps(salir).encode(), (SERVER_IP, SERVER_PORT))
                
                if (self.carpeta_usuario.exists()): # Si existe se borra
                        time.sleep(0.5)  # medio segundo de espera
                        shutil.rmtree(self.carpeta_usuario) # Se borra la carpeta del usuario
                
                self.activo = False
                sys.exit(0)

    def iniciar(self) -> None:
        """Método para inicializar los hilos. Un hilo para recibir mensajes en segundo plano y uno principal para enviar."""
        threading.Thread(target=self.recibir_mensaje, daemon=True).start()
        self.enviar_mensaje()

def main() -> None:
    usuario = input("Antes de unirte a la sala, escribe tu nombre de usuario:\nUsuario: ")
    cliente = Cliente(usuario, "general")
    cliente.iniciar()

if (__name__ == "__main__"):
    main()