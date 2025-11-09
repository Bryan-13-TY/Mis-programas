"""
Servidor para el chat.

Se cuentan con las funciones para enviar mensajes a usuarios especificos
en cualquier sala, para enviar mensajes a todos los usuarios en una sala y también
para manejar los tipos de mensajes que se envían desde los usuarios y a los usuarios. 

Autores:
    - García Escamilla Bryan Alexis
    - Meléndez Macedonio Rodrigo

Fecha: 08/11/2025
"""
import socket
import json
import threading

# colores ANSI
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

HOST, PORT = "0.0.0.0", 5007 # el servidor escucha en todas las interfaces en el puerto 5007
usuarios = {"general": {}} # lista de usuarios por sala: {"general": {"usuario": (ip, puerto)}}
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # se crea un socket UDP
sock.bind((HOST, PORT)) # se vincula el socket al puerto del servidor

print("Servidor de chat activo...")

def enviar_unicast(data: dict, addr: tuple) -> None:
    """
    Envía un mensaje a un cliente específico.

    Parameters
    ----------
    data : dict
        Metadatos a enviar al usuario.
    addr : tuple
        (direccion_IP, puerto)

        - **direccion_IP** (str): Dirección IP del usuario.
        - **puerto** (int): Puerto del usuario.
    """
    sock.sendto(json.dumps(data).encode(), addr)


def enviar_publico(data: dict, sala: str) -> None:
    """
    Envía un mensaje a cada uno de los usuarios de la sala.

    Parameters
    ----------
    data : dict
        Metadatos a enviar a cada usuario.
    sala : str
        Sala a la que se envían los metadatos.
    """
    for usuario_addr in usuarios[sala].values():
        enviar_unicast(data, usuario_addr)


def manejar_cliente() -> None:
    """Bucle principal del servidor para recibir mensajes del cliente."""
    while True:
        data, addr = sock.recvfrom(4096) # recibe datagramas de cualquier cliente.
        try:
            mensaje = json.loads(data.decode()) # se decodifica el mensaje en JSON
        except:
            # se ignora si la decodificación falla
            continue

        tipo = mensaje.get("tipo")
        usuario = mensaje.get("user")
        sala = mensaje.get("sala", "general")

        # ---- 1. se solicita la lista de salas disponibles ----
        if tipo == "listar_salas":
            salas = list(usuarios.keys())
            respuesta = {"tipo": "salas",
                         "lista": salas}
            
            enviar_unicast(respuesta, addr)
            continue

        # ---- 2. se crea la sala si no existe ----
        if sala not in usuarios:
            usuarios[sala] = {}
        
        # ---- 3. un usuario entra a la sala ----
        if tipo == "inicio":
            if usuario not in usuarios[sala]: # si el usuario no esta en la sala anteriormente
                usuarios[sala][usuario] = addr # se agrega el usuario a la sala (se guarda la IP y puerto del usuario)
                aviso = {"tipo": "aviso",
                         "sala": sala,
                         "content": f">> {GREEN}[+]{RESET}{BLUE}[{usuario}]{RESET} se ha unido a la sala"}
                
                enviar_publico(aviso, sala)

            # se actualiza la lista de usuarios conectados en la sala
            usuarios_sala = {"tipo": "usuarios",
                             "sala": sala,
                             "lista": list(usuarios[sala].keys())}
            
            enviar_publico(usuarios_sala, sala)

        # ---- 4. mensaje ----
        elif tipo == "msj":
            # ---- 4.1. mensaje público ----
            if not mensaje.get("privado", False):
                enviar_publico(mensaje, sala)
            # ---- 4.2.- mensaje privado ----
            elif mensaje.get("privado", False):
                dest = mensaje.get("to") # se extre al destinatario del mensaje

                if dest in usuarios[sala]: # si el destinatario esta en la sala
                    enviar_unicast(mensaje, usuarios[sala][dest])
                else: # si el destinatario no esta en la sala
                    error = {"tipo": "aviso",
                             "sala": sala,
                             "content": f">> {RED}[system]{RESET} Usuario '{dest}' no está conectado"}
                    
                    enviar_unicast(error, addr)

        # ---- 5. un usuario abandona la sala ----
        elif tipo == "salir":
            if usuario in usuarios[sala]: # si el usuario esta actualmente en la sala
                usuarios[sala].pop(usuario) # se elimina el usuario de la sala                
                aviso = {"tipo": "aviso",
                         "sala": sala,
                         "content": f">> {RED}[-]{RESET}{BLUE}[{usuario}]{RESET} ha abandonado la sala"}
                
                enviar_publico(aviso, sala)

            # se actualiza la lista de usuarios conectados en la sala
            usuarios_sala = {"tipo": "usuarios",
                             "sala": sala,
                             "lista": list(usuarios[sala].keys())}
            
            enviar_publico(usuarios_sala, sala)

        # ---- 6. audio ----
        elif tipo == "audio":
            # ---- 6.1. audio público ----
            if not mensaje.get("privado", False):
                aviso = {"tipo": "aviso",
                         "sala": sala,
                         "content": f"{GREEN}[🎙️][{usuario}]{RESET} ha enviado el audio '{mensaje.get("nombre")}'"}
                
                enviar_publico(aviso, sala)
            # ---- 6.2. audio privado ----
            elif mensaje.get("privado", False):
                dest = mensaje.get("to") # se extre al destinatario del mensaje

                if dest in usuarios[sala]: # si el destinatario esta en la sala
                    enviar_unicast(mensaje, usuarios[sala][dest])
                else:
                    error = {"tipo": "aviso",
                             "sala": sala,
                             "content": f">> {RED}[system]{RESET} Usuario '{dest}' no está conectado"}
                    
                    enviar_unicast(error, addr)


def main() -> None:
    threading.Thread(target=manejar_cliente, daemon=True).start() # Hilo principal del servidor

    while True: # mantener el servidor activo
        pass

if __name__ == "__main__":
    main()