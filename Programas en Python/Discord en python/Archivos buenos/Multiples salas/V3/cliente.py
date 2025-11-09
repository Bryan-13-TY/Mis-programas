"""
Clase 'Cliente' que representa a un usuario en una sala.

Se cuentan con los métodos para enviar menasajes al servidor y para recibirlos
desde el servidor y también para buscar un sticker, y por último una función
para obtener las salas activas.

Autores:
    - García Escamilla Bryan Alexis
    - Meléndez Macedonio Rodrigo

Fecha: 08/11/2025
"""
import socket
import threading
import json
import sys
import os
from pathlib import Path

from audio import Audio

# Colores ANSI
RED = "\033[91m"
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
        self.audio = Audio() # objeto de tipo audio

        # se crea el socket UDP para enviar y recibir mensajes
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # se crea un socket UDP
        self.sock.bind(('', 0))  # puerto aleatorio para recibir mensajes
        
        self.carpeta_script = Path(__file__).parent
        self.carpeta_sala = self.carpeta_script / f"{self.sala}" # carpeta de la sala
        self.carpeta_sala.mkdir(parents=True, exist_ok=True)
        self.carpeta_usuario = self.carpeta_sala / f"{self.usuario}" # carpeta del usuario
        self.carpeta_usuario.mkdir(parents=True, exist_ok=True)

        # avisar al servidor que un usuario entro a la sala
        inicio = {"tipo": "inicio",
                  "user": self.usuario,
                  "sala": self.sala}
        
        self.sock.sendto(json.dumps(inicio).encode(), (SERVER_IP, SERVER_PORT))

    def buscar_sticker(self, nombre_sticker: str) -> str:
        """
        Método que devuelve el sticker elegido por el usuario.
        
        Parameters
        ----------
        nombre_sticker : str
            Nombre del sticker que se quiere enviar.
        
        Returns
        -------
        str
            Sticker seleccionado por el usuario.
        """
        match nombre_sticker:
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
        while self.activo: # mientras el usuario siga en una sala
            try:
                data, _ = self.sock.recvfrom(4096)
                mensaje = json.loads(data.decode())
                sala_mensaje = mensaje.get("sala", self.sala)
                tipo = mensaje.get("tipo")

                if sala_mensaje != self.sala:
                    # si el mensaje no se envía a la sala actual se ignora
                    continue

                if tipo == "msj":
                    if mensaje.get("privado"): # mensaje privado
                        print(f"{YELLOW}[Privado de {mensaje['from']}]{RESET}: {mensaje['content']}")
                    else: # mensaje público
                        print(f"{BLUE}[{mensaje['user']}]{RESET}: {mensaje['content']}")
                
                if tipo == "aviso":
                    print(mensaje["content"])

                if tipo == "audio": # audio privado
                    print(f"{YELLOW}[Privado de {mensaje['from']}]{RESET}: {mensaje['content']}")
                
                if tipo == "usuarios":
                    print(f"Usuarios en sala {MAGENTA}'{self.sala}'{RESET}: {MAGENTA}{', '.join(mensaje['lista'])}{RESET}")
            except:
                break

    def enviar_mensaje(self) -> None:
        """Método para enviar mensajes al servidor."""
        while self.activo: # mientras el usuario siga en una sala
            try:
                texto = input("").strip()
                
                # ---- 1. usuario sale de la sala ----
                if texto.lower() == "/salir":
                    salir = {"tipo": "salir",
                             "user": self.usuario,
                             "sala": self.sala}
                    
                    self.sock.sendto(json.dumps(salir).encode(), (SERVER_IP, SERVER_PORT))        
                    self.activo = False
                    
                    print(f">> {RED}[system]{RESET} Has salido de la sala")
                    break

                # ---- 2. usuario envía un audio público ----
                elif texto.lower() == "/audio":
                    audio = {"tipo": "audio",
                             "privado": False,
                             "user": self.usuario,
                             "sala": self.sala}
                    
                    nombre_audio = self.audio.grabar_audio(audio, self.carpeta_script, self.sala, self.usuario)
                    audio.update({"nombre": nombre_audio})
                    self.sock.sendto(json.dumps(audio).encode(), (SERVER_IP, SERVER_PORT))
                
                # ---- 3. usuario envía un sticker público ----
                elif texto.lower().startswith("/sticker"):
                    partes = texto.split(" ", 1)

                    if len(partes) < 2: # el formato no es el correcto
                        print(f">> {RED}[system]{RESET} Formato: /sticker nombre_sticker")
                        continue

                    _, nombre_sticker = partes
                    sticker = self.buscar_sticker(nombre_sticker)

                    if not sticker: # Si el sticker no existe
                        print(f">> {RED}[system]{RESET} El sticker no existe")
                        continue

                    mensaje = {"tipo": "msj",
                               "privado": False,
                               "user": self.usuario,
                               "sala": self.sala,
                               "content": sticker}
                    
                    self.sock.sendto(json.dumps(mensaje).encode(), (SERVER_IP, SERVER_PORT))
                
                # ---- 4. usuario reproduce un audio ----
                elif texto.lower().startswith("/reproducir"):
                    partes = texto.split(" ", 1)

                    if len(partes) < 2: # el formato no es el correcto
                        print(f">> {RED}[system]{RESET} Formato: /reproducir nombre_archivo")
                        continue

                    _, nombre_archivo = partes # Se obtiene el nombre del audio grabado
                    ruta_audio = self.audio.buscar_audio(self.carpeta_sala, self.carpeta_usuario, self.usuario, nombre_archivo)

                    if ruta_audio: # Si existe el audio
                        self.audio.reproducir_audio(ruta_audio, nombre_archivo)
                    else:
                        print(f">> {RED}[system]{RESET} El audio no existe")

                # ---- 5. mensajes privados ----
                elif texto.startswith("@"):
                    partes = texto.split(" ", 1)
                    
                    if len(partes) < 2: # el formato no es el correcto
                        print(f">> {RED}[system]{RESET} Formato: @usuario mensaje")
                        continue

                    # ---- 5.1. usuario envía un sticker privado
                    if partes[1].startswith("/sticker"):
                        partes2 = partes[1].split(" ")

                        if len(partes2) < 2: # el formato no es correcto
                            print(f">> {RED}[system]{RESET} Formato: /sticker nombre_sticker")
                            continue

                        _, nombre_sticker = partes2
                        sticker = self.buscar_sticker(nombre_sticker)

                        if not sticker: # si el sticker no existe
                            print(f">> {RED}[system]{RESET} El sticker no existe")
                            continue

                        destinatario, _ = partes
                        destinatario = destinatario[1:] # quitar '@'
                        mensaje = {"tipo": "msj",
                                   "privado": True,
                                   "from": self.usuario,
                                   "to": destinatario,
                                   "content": sticker,
                                   "sala": self.sala}
                        
                        self.sock.sendto(json.dumps(mensaje).encode(), (SERVER_IP, SERVER_PORT))
                    
                        print(f"{ORANGE}[Tú -> {destinatario}]{RESET}: {sticker}")
                        continue
                    
                    # ---- 5.2. usuario envía un audio privado ----
                    elif partes[1] == "/audio":
                        destinatario, _ = partes
                        destinatario = destinatario[1:] # quitar '@'
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

                    # ---- 5.3. usuario envía un mensaje privado
                    else:
                        destinatario, contenido = partes
                        destinatario = destinatario[1:] # quitar '@'
                        mensaje = {"tipo": "msj",
                                "privado": True,
                                "from": self.usuario,
                                "to": destinatario,
                                "content": contenido,
                                "sala": self.sala}
                        
                        self.sock.sendto(json.dumps(mensaje).encode(), (SERVER_IP, SERVER_PORT))
                        
                        print(f"{ORANGE}[Tú -> {destinatario}]{RESET}: {contenido}")
                        continue
                
                # ---- 6. usuario envía un mensaje público
                else:
                    mensaje = {"tipo": "msj",
                               "privado": False,
                               "user": self.usuario,
                               "sala": self.sala,
                               "content": texto}
                    
                    self.sock.sendto(json.dumps(mensaje).encode(), (SERVER_IP, SERVER_PORT))
            except KeyboardInterrupt: # el usuario presiona Ctrl + C (salir de la sala)
                salir = {"tipo": "salir",
                         "user": self.usuario,
                         "sala": self.sala}
                
                self.sock.sendto(json.dumps(salir).encode(), (SERVER_IP, SERVER_PORT))        
                self.activo = False
                sys.exit(0)
    
    def iniciar(self) -> None:
        """Método para inicializar los hilos. Un hilo para recibir mensajes en segundo plano y uno principal para enviar."""
        threading.Thread(target=self.recibir_mensaje, daemon=True).start()
        self.enviar_mensaje()


def limpiarTerminal() -> None:
    """
    Limpia la terminal de cualquier sistema operativo. 
    """
    os.system('cls' if os .name == 'nt' else 'clear')


def obtener_salas() -> list:
    """Solicita la lista de salas al servidor."""
    temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    temp_sock.bind(('', 0))

    peticion = {"tipo": "listar_salas"}
    
    temp_sock.sendto(json.dumps(peticion).encode(), (SERVER_IP, SERVER_PORT))

    data, _ = temp_sock.recvfrom(4096)
    temp_sock.close()

    try:
        respuesta = json.loads(data.decode())
        return respuesta["lista"] if respuesta["tipo"] == "salas" else []
    except:
        return []
    

def main() -> None:
    print(f">> {RED}[system]{RESET} Obteniendo salas disponibles...\n")

    salas_disponibles = obtener_salas()
    if salas_disponibles: # hay salas disponibles
        print("Salas disponibles:")

        for i, s in enumerate(salas_disponibles, 1):
            print(f"{i}. {s}")
    else:
        print(f">> {RED}[system]{RESET} No hay salas actvas. Se creará una nueva sala al unirte")

    sala = input("\nEscribe el nombre de la sala a la que desesar unirte (o crea una nueva): ").strip()
    if not sala:
        sala = "general"

    usuario = input("Ingresa tu nombre de usuario: ")
    
    limpiarTerminal()
    print(f"""
====================================
 BIENVENIDO A LA SALA '{sala}'
====================================
 USUARIO: {usuario}
========================
""")

    cliente = Cliente(usuario, sala)
    cliente.iniciar()

if __name__ == "__main__":
    main()