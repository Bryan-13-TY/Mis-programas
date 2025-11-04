import socket, struct, json

MULTICAST_GRP, PORT = ("224.1.1.1", 5007) # Grupo multicast y el puerto
# Las direcciones 224.0.0.0 - 239.255.255.255 son reservadas para multicast

# Ahora guardaremos usuarios como: {"general": {"Bryan": ("192.168.1.10", 54321)}}
usuarios = {"general": {}} # Diccionario para la lista de usuarios por sala (por el momento solo la sala general)

# Creación del socket UDP multicast
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # Creación del socket UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Permite que varios sockets se vinculen al mismo puerto
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
sock.bind(('', PORT)) # Asocia el socket al puerto 5007 en todas las interfaces de red

# Unirse al grupo multicast
grupo = socket.inet_aton(MULTICAST_GRP) # Convierte la IP multicast a formato binario
mreq = struct.pack('4sL', grupo, socket.INADDR_ANY) # Grupo multicast (4 bytes), cualquier interfaz disponible (entero largo)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq) # Hace que el socket se unaa al grupo multicast, recibiendo los mensajes enviados al grupo 224.1.1.1

print("Servidor de chat multicast activo...")

def enviar_multicast(data: dict) -> None:
    """
    Envía un mensaje a todos los usuarios mediante multicast.

    Parameters
    ----------
    data : dict
        Mensaje a enviar a todos los usuarios mendiante multicast.
    """
    sock.sendto(json.dumps(data).encode(), (MULTICAST_GRP, PORT))

def enviar_unicast(data: dict, addr: tuple) -> None:
    """
    Envía un mensaje directamente a un usuario.

    Parameters
    ----------
    data : dict
        Mensaje a enviar directamente a un usuario.
    addr : tuple
        Tupla con la dirección IP y puerto del usaurio.
    """
    sock.sendto(json.dumps(data).encode(), addr)

while (True):
    data, addr = sock.recvfrom(1024) # Espera a recibir un datagrama UDP (1024 bytes)
    msj = json.loads(data.decode()) # Decodifica el mensaje recibido
    tipo = msj.get("tipo")
    user = msj.get("user")
    sala = msj.get("sala", "general")

    # El usuario se una a la sala
    if (tipo == "inicio"): # Si se trata de un nuevo usuario que se conecta a una sala
        if (user not in usuarios[sala]): # Busca duplicados del usuario en la sala
            usuarios[sala][user] = addr # Agrega al usuario a la sala (guarda IP y puerto del usuario)

            # Aviso de entrada
            aviso = {"tipo": "aviso", "sala": sala, "content": f"[+][{user}] se ha unido a la sala"}
            enviar_multicast(aviso)

        # Enviar lista actualizada
        lista = {"tipo": "usuarios", "sala": sala, "lista": list(usuarios[sala].keys())} # Lista actualizada de usuarios en la sala
        enviar_multicast(lista)
    elif (tipo == "msj"):
        if (msj.get("privado", False)):
            # Mensaje privado
            destino = msj.get("to")

            if (destino in usuarios[sala]):
                enviar_unicast(msj, usuarios[sala][destino])
            else:
                error = {"tipo": "aviso", "sala": sala, "content": f"[Sistema] El usuario '{destino}' no está conectado."}
                enviar_unicast(error, addr)
        else:
            # Mensaje público
            enviar_multicast(msj)
    # El usuario abandona la sala
    elif (tipo == "salir"):
        if (user in usuarios[sala]): # Se busca el usuario en la sala
            usuarios[sala].pop(user) # Elimina al usuario de la sala

            # Aviso de salida
            aviso = {"tipo": "aviso", "sala": sala, "content": f"[-][{user}] ha abandonado la sala"}
            enviar_multicast(aviso)

        # Enviar la lista actualizada
        lista = {"tipo": "usuarios", "sala": sala, "lista": list(usuarios[sala].keys())} # Lista actualizada de usuarios en la sala
        enviar_multicast(lista)