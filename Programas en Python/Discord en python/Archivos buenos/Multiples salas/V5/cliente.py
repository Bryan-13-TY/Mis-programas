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
from pathlib import Path

from audio import Audio
from stickers import obtener_sticker
import utils as utl

SERVER = ("127.0.0.1", 5007)  # IP y puerto del servidor

class Cliente:
    def __init__(self, usuario: str, sala: str) -> None:
        """
        Constructor de la clase.

        Parameters
        ----------
        usuario : str
            Nombre de usuario del cliente.
        sala : str
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
        
        self.sock.sendto(json.dumps(inicio).encode(), SERVER)

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
                        print(f"{utl.YELLOW}[Privado de {mensaje['from']}]{utl.RESET}: {mensaje['content']}")
                    else: # mensaje público
                        print(f"{utl.BLUE}[{mensaje['user']}]{utl.RESET}: {mensaje['content']}")
                
                if tipo == "aviso":
                    print(mensaje["content"])

                if tipo == "audio": # audio privado
                    print(f"{utl.YELLOW}[Privado de {mensaje['from']}]{utl.RESET}: {mensaje['content']}")
                
                if tipo == "usuarios":
                    print(f"Usuarios en sala {utl.MAGENTA}'{self.sala}'{utl.RESET}: {utl.MAGENTA}{', '.join(mensaje['lista'])}{utl.RESET}")
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
                    
                    self.sock.sendto(json.dumps(salir).encode(), SERVER)        
                    self.activo = False
                    
                    print(f">> {utl.RED}[system]{utl.RESET} Has salido de la sala")
                    self.sock.close()
                    break

                # ---- 2. usuario envía un audio público ----
                elif texto.lower() == "/audio":
                    audio = {"tipo": "audio",
                             "privado": False,
                             "user": self.usuario,
                             "sala": self.sala}
                    
                    nombre_audio = self.audio.grabar_audio(audio, self.carpeta_script, self.sala, self.usuario)
                    audio.update({"nombre": nombre_audio})
                    self.sock.sendto(json.dumps(audio).encode(), SERVER)
                
                # ---- 3. usuario envía un sticker público ----
                elif texto.lower().startswith("/sticker"):
                    partes = texto.split(" ", 1)

                    if len(partes) < 2: # el formato no es el correcto
                        print(f">> {utl.RED}[system]{utl.RESET} Formato: /sticker nombre_sticker")
                        continue

                    _, nombre_sticker = partes
                    sticker = obtener_sticker(nombre_sticker)

                    if not sticker: # Si el sticker no existe
                        print(f">> {utl.RED}[system]{utl.RESET} El sticker no existe")
                        continue

                    mensaje = {"tipo": "msj",
                               "privado": False,
                               "user": self.usuario,
                               "sala": self.sala,
                               "content": sticker}
                    
                    self.sock.sendto(json.dumps(mensaje).encode(), SERVER)
                
                # ---- 4. usuario reproduce un audio ----
                elif texto.lower().startswith("/reproducir"):
                    partes = texto.split(" ", 1)

                    if len(partes) < 2: # el formato no es el correcto
                        print(f">> {utl.RED}[system]{utl.RESET} Formato: /reproducir nombre_archivo")
                        continue

                    _, nombre_archivo = partes # Se obtiene el nombre del audio grabado
                    ruta_audio = self.audio.buscar_audio(self.carpeta_sala, self.carpeta_usuario, self.usuario, nombre_archivo)

                    if ruta_audio: # Si existe el audio
                        self.audio.reproducir_audio(ruta_audio, nombre_archivo)
                    else:
                        print(f">> {utl.RED}[system]{utl.RESET} El audio no existe")

                # ---- 5. mensajes privados ----
                elif texto.startswith("@"):
                    partes = texto.split(" ", 1)
                    
                    if len(partes) < 2: # el formato no es el correcto
                        print(f">> {utl.RED}[system]{utl.RESET} Formato: @usuario mensaje")
                        continue

                    # ---- 5.1. usuario envía un sticker privado
                    if partes[1].startswith("/sticker"):
                        partes2 = partes[1].split(" ")

                        if len(partes2) < 2: # el formato no es correcto
                            print(f">> {utl.RED}[system]{utl.RESET} Formato: /sticker nombre_sticker")
                            continue

                        _, nombre_sticker = partes2
                        sticker = obtener_sticker(nombre_sticker)

                        if not sticker: # si el sticker no existe
                            print(f">> {utl.RED}[system]{utl.RESET} El sticker no existe")
                            continue

                        destinatario, _ = partes
                        destinatario = destinatario[1:] # quitar '@'
                        mensaje = {"tipo": "msj",
                                   "privado": True,
                                   "from": self.usuario,
                                   "to": destinatario,
                                   "content": sticker,
                                   "sala": self.sala}
                        
                        self.sock.sendto(json.dumps(mensaje).encode(), SERVER)
                    
                        print(f"{utl.ORANGE}[Tú -> {destinatario}]{utl.RESET}: {sticker}")
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
                        self.sock.sendto(json.dumps(audio).encode(), SERVER)

                        print(f"{utl.ORANGE}[Tú -> {destinatario}]{utl.RESET}: has enviado el audio '{nombre_audio}'")
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
                        
                        self.sock.sendto(json.dumps(mensaje).encode(), SERVER)
                        
                        print(f"{utl.ORANGE}[Tú -> {destinatario}]{utl.RESET}: {contenido}")
                        continue
                
                # ---- 6. usuario envía un mensaje público
                else:
                    mensaje = {"tipo": "msj",
                               "privado": False,
                               "user": self.usuario,
                               "sala": self.sala,
                               "content": texto}
                    
                    self.sock.sendto(json.dumps(mensaje).encode(), SERVER)
            except KeyboardInterrupt: # el usuario presiona Ctrl + C (salir de la sala)
                salir = {"tipo": "salir",
                         "user": self.usuario,
                         "sala": self.sala}
                
                self.sock.sendto(json.dumps(salir).encode(), SERVER)        
                self.activo = False
                self.sock.close()
                sys.exit(0)
    
    def iniciar(self) -> None:
        """Método para inicializar los hilos. Un hilo para recibir mensajes en segundo plano y uno principal para enviar."""
        threading.Thread(target=self.recibir_mensaje, daemon=True).start()
        self.enviar_mensaje()

def obtener_salas() -> list:
    """Solicita la lista de salas al servidor."""
    temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    temp_sock.bind(('', 0))

    peticion = {"tipo": "listar_salas"}
    
    temp_sock.sendto(json.dumps(peticion).encode(), SERVER)

    data, _ = temp_sock.recvfrom(4096)
    temp_sock.close()

    try:
        respuesta = json.loads(data.decode())
        return respuesta["lista"] if respuesta["tipo"] == "salas" else []
    except:
        return []
    

def main() -> None:
    print(f">> {utl.RED}[system]{utl.RESET} Obteniendo salas disponibles...\n")

    salas_disponibles = obtener_salas()
    if salas_disponibles: # hay salas disponibles
        print("Salas disponibles:")

        for i, s in enumerate(salas_disponibles, 1):
            print(f"{i}. {s}")
    else:
        print(f">> {utl.RED}[system]{utl.RESET} No hay salas actvas. Se creará una nueva sala al unirte")

    sala = input("\nEscribe el nombre de la sala a la que desesar unirte (o crea una nueva): ").strip()
    if not sala:
        sala = "general"

    usuario = input("Ingresa tu nombre de usuario: ")
    
    utl.limpiar_terminal()
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