import socket, json, threading, os

RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Dirección y puerto del servidor
HOST, PORT = "0.0.0.0", 5007 # El servidor escucha en todas las interfaces y en el puerto 5007
usuarios = {"general": {}} # Lista de usuarios por sala: {"general": {"usuario": (ip, puerto)}}

# Crear socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Se crea un socket UDP
sock.bind((HOST, PORT)) # Se vincula el socket al puerto del servidor

print("Servidor de chat unicast activo...")

def limpiar_terminal() -> None:
    """
    Limpia la terminal de cualquier sistema operativo. 
    """
    os.system('cls' if os .name == 'nt' else 'clear')

def enviar_unicast(data: dict, addr: tuple) -> None:
    """
    Envía un mensaje a un cliente específico
    
    Parameters
    ----------
    data : dict
        Mensaje a enviar al cliente.
    addr : tuple
        Dirección IP y puerto del usuario.
    """
    sock.sendto(json.dumps(data).encode(), addr)

def enviar_publico(data: dict, sala: str):
    """
    Envía un mensaje a todos los usuarios de la sala
    
    Parameters
    ----------
    data : dict
        Mensaje a enviar a todos los usuarios de la sala.
    sala : str
        Sala a la que se envía el mensaje.
    """
    for user_addr in usuarios[sala].values():
        enviar_unicast(data, user_addr)

def manejar_cliente() -> None:
    """
    Loop principal del servidor para recibir mensajes
    """
    while (True):
        data, addr = sock.recvfrom(4096) # Recibe datagramas de cualquier cliente.
        try:
            msj = json.loads(data.decode()) # Se decodifica el mensaje en JSON
        except:
            # Se ignora si la decodificación falla
            continue

        tipo = msj.get("tipo") # Se estrae el tipo del mensaje
        user = msj.get("user") # Se extrae el usuario que envía el mensaje
        sala = msj.get("sala", "general") # Se extrae la sala a la que se envía el mensaje

        # Crear sala si no existe
        if (sala not in usuarios):
            usuarios[sala] = {}

        # Usuario entra a la sala
        if (tipo == "inicio"):
            if (user not in usuarios[sala]): # Si el usuario no esta en la sala anteriormente
                usuarios[sala][user] = addr # Se agrega el usuario a la sala (se guarda la IP y puerto del usuario)

                aviso = {"tipo": "aviso", "sala": sala, "content": f"{GREEN}[+]{RESET}{BLUE}[{user}]{RESET} se ha unido a la sala"}
                
                enviar_publico(aviso, sala) # Se envía el aviso de entrada de un usuario

            # Si el usuario ya se encuentra en la sala solo se envía la lista de usuarios actual
            lista = {"tipo": "usuarios", "sala": sala, "lista": list(usuarios[sala].keys())}
            
            enviar_publico(lista, sala) # Se envía la lista actualizada
        # Mensaje público
        elif (tipo == "msj" and not msj.get("privado", False)):
            enviar_publico(msj, sala)
        # Mensaje privado
        elif (tipo == "msj" and msj.get("privado", False)):
            destino = msj.get("to")
            
            if (destino in usuarios[sala]): # Si es destinatario esta en la sala
                enviar_unicast(msj, usuarios[sala][destino]) # Se envía el mensaje al destinatario
                #enviar_unicast(msj, addr) # Se envía una copia del mensaje al remitente
            else: # Si el destinatario no esta en la sala
                error = {"tipo": "aviso", "sala": sala, "content": f"[Sistema] Usuario '{destino}' no está conectado."}
                
                enviar_unicast(error, addr) # Se envía un mensaje de error
        # Usuario sale
        elif (tipo == "salir"):
            if (user in usuarios[sala]): # Si el usuario se encuentra en la sala
                usuarios[sala].pop(user) # Se elimina el usuario de la sala
                
                aviso = {"tipo": "aviso", "sala": sala, "content": f"{RED}[-]{RESET}{BLUE}[{user}]{RESET} ha abandonado la sala"}
                
                enviar_publico(aviso, sala) # Se envía el aviso de salida de un usuario

            lista = {"tipo": "usuarios", "sala": sala, "lista": list(usuarios[sala].keys())}
            
            enviar_publico(lista, sala) # Se envía la lista actualizada
        # Usuario graba audio
        elif (tipo == "audio"):
            aviso = {"tipo": "aviso", "sala": sala, "content": f"{GREEN}[🎙️][{user}]{RESET} ha enviado un audio"}

            enviar_publico(aviso, sala)

def main() -> None:
    # Hilo principal del servidor
    threading.Thread(target=manejar_cliente, daemon=True).start()

    # Mantener el servidor activo
    while True:
        pass

if (__name__ == "__main__"):
    main()