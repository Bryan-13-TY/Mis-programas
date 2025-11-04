import socket, json, threading

# Colores ANSI
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Dirección y puerto del servidor
HOST, PORT = "0.0.0.0", 5007 # El servidor escucha en todas las interfaces y en el puerto 5007
usuarios = {"general": {}} # Lista de usuarios por sala: {"general": {"usuario": (ip, puerto)}}

# Se crea el socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Se crea un socket UDP
sock.bind((HOST, PORT)) # Se vincula el socket al puerto del servidor

print("Servidor de chat activo...")

def enviar_unicast(data: dict, addr: tuple) -> None:
    """
    Envía un mensaje a un cliente específico.
    
    Parameters
    ----------
    data : dict
        Mensaje a enviar al cliente.
    addr : tuple
        Dirección IP y puerto del usuario.
    """
    sock.sendto(json.dumps(data).encode(), addr)

def enviar_publico(data: dict, sala: str) -> None:
    """
    Envía un mensaje a todos los usuarios de la sala.
    
    Parameters
    ----------
    data : dict
        Mensaje a enviar a todos los usuarios de la sala.
    sala : str
        Sala a la que se envía el mensaje.
    """
    # Se envía el mensaje a cada usuario conectado en la sala
    for user_addr in usuarios[sala].values():
        enviar_unicast(data, user_addr)

def manejar_cliente() -> None:
    """Bucle principal del servidor para recibir mensajes del cliente."""
    while (True):
        data, addr = sock.recvfrom(4096) # Recibe datagramas de cualquier cliente.

        try:
            mensaje = json.loads(data.decode()) # Se decodifica el mensaje en JSON
        except:
            # Se ignora si la decodificación falla
            continue

        tipo = mensaje.get("tipo") # Se extrae el tipo del mensaje
        usuario = mensaje.get("user") # Se extrae el usuario que envía el mensaje
        sala = mensaje.get("sala", "general") # Se extrae la sala desde donde se envía el mensaje

        if (sala not in usuarios): # Se crea la sala si no existe
            usuarios[sala] = {}

        if (tipo == "inicio"): # Usuario entra a la sala
            if (usuario not in usuarios[sala]): # Si el usuario no estaba en la sala anteriormente
                usuarios[sala][usuario] = addr # Se agrega al usuario a la sala (se guarda la IP y puerto)

                aviso = {"tipo": "aviso",
                         "sala": sala,
                         "content": f"{GREEN}[+]{RESET}{BLUE}[{usuario}]{RESET} se ha unido a la sala"}
                
                enviar_publico(aviso, sala) # Se envía el aviso de entrada de un usuario a todos los usuarios en la sala

            # Se actualiza la lista de usuarios conectados en la sala
            usuarios_conectados = {"tipo": "usuarios",
                                   "sala": sala,
                                   "lista": list(usuarios[sala].keys())}
            
            enviar_publico(usuarios_conectados, sala) # Se envía la lista de usuarios conectados actualizada
        
        elif (tipo == "msj" and not mensaje.get("privado", False)): # Si el mensaje es público
            enviar_publico(mensaje, sala) # Se envía el mensaje normal
        
        elif (tipo == "msj" and mensaje.get("privado", False)): # Si el mensaje es privado
            destinatario = mensaje.get("to") # Se extrae el destinatario

            if (destinatario in usuarios[sala]): # Si el destinatario esta en la sala
                enviar_unicast(mensaje, usuarios[sala][destinatario]) # Se envía el mensaje al destinatario
            else: # Si el destinatario no esta en la sala
                error = {"tipo": "aviso",
                         "sala": sala,
                         "content": f"[Sistema] '{destinatario} no está conectado'"}
                
                enviar_unicast(error, addr) # Se envía el mensaje de error

        elif (tipo == "salir"): # Si el usuario abandona la sala
            if (usuario in usuarios[sala]): # Si el usuario esta actualmente en la sala
                usuarios[sala].pop(usuario) # Se elimina el usuario de la sala

                aviso = {"tipo": "aviso",
                         "sala": sala,
                         "content": f"{RED}[-]{RESET}[{usuario}]{RESET} ha abandonado la sala"}
                
                enviar_publico(aviso, sala) # Se envía el aviso de salida de un usuario a todos los usuarios en la sala

            # Se actualiza la lista de usuarios conectados en la sala
            usuarios_conectados = {"tipo": "usuarios",
                                   "sala": sala,
                                   "lista": list(usuarios[sala].keys())}
            
            enviar_publico(usuarios_conectados, sala) # Se envía la lista de usuarios conectados actualizada
        
        elif (tipo == "audio"): # Si el usuario envía un audio
            aviso = {"tipo": "aviso",
                     "sala": sala,
                     "content": f"{GREEN}[🎙️][{usuario}]{RESET} ha enviado un audio"}
            
            enviar_publico(aviso, sala) # Se envía el aviso de envío de audio a todos los usuarios en la sala

def main() -> None:
    threading.Thread(target=manejar_cliente, daemon=True).start() # Hilo principal del servidor

    while (True): # Mantener el servidor activo
        pass

if (__name__ == "__main__"):
    main()