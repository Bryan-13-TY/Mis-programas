import socket, struct, json

MULTICAST_GRP, PORT = ("224.1.1.1", 5007) # Grupo multicast y el puerto
# Las direcciones 224.0.0.0 - 239.255.255.255 son reservadas para multicast

usuarios = {"general": []} # Diccionario para la lista de usuarios por sala (por el momento solo la sala general)

# Creación del socket UDP multicast
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # Creación del socket UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Permite que varios sockets se vinculen al mismo puerto
sock.bind(('', PORT)) # Asocia el socket al puerto 5007 en todas las interfaces de red

# Unirse al grupo multicast
grupo = socket.inet_aton(MULTICAST_GRP) # Convierte la IP multicast a formato binario
mreq = struct.pack('4sL', grupo, socket.INADDR_ANY) # Grupo multicast (4 bytes), cualquier interfaz disponible (entero largo)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq) # Hace que el socket se unaa al grupo multicast, recibiendo los mensajes enviados al grupo 224.1.1.1

print("Servidor de chat multicast activo...")

def enviar_mensaje(data: dict) -> None:
    """
    Envía un mensaje JSON a todos los usurios en el grupo multicast.

    Parameters
    ----------
    data : dict
        Datos a envíar a todos los usuarios en el grupo multicast.
    """
    sock.sendto(json.dumps(data).encode(), (MULTICAST_GRP, PORT))

while (True):
    data, addr = sock.recvfrom(1024) # Espera a recibir un datagrama UDP (1024 bytes)
    msj = json.loads(data.decode()) # Decodifica el mensaje recibido
    tipo = msj.get("tipo")
    user = msj.get("user")
    sala = msj.get("sala", "general")

    # El usuario se una a la sala
    if (tipo == "inicio"): # Si se trata de un nuevo usuario que se conecta a una sala
        if (user not in usuarios[sala]): # Busca duplicados del usuario en la sala
            usuarios[sala].append(user) # Agrega al usuario a la sala

            # Aviso de entrada
            aviso = {"tipo": "aviso", "sala": sala, "content": f"[+][{user}] se ha unido a la sala"}
            enviar_mensaje(aviso)

        # Enviar lista actualizada
        lista = {"tipo": "usuarios", "sala": sala, "lista": usuarios[sala]} # Lista actualizada de usuarios en la sala
        enviar_mensaje(lista)
    # El usuarios abandona la sala
    elif (tipo == "salir"):
        if (user in usuarios[sala]): # Se busca el usuario en la sala
            usuarios[sala].remove(user) # Elimina al usuario de la sala

            # Aviso de salida
            aviso = {"tipo": "aviso", "sala": sala, "content": f"[-][{user}] ha abandonado la sala"}
            enviar_mensaje(aviso)

        # Enviar la lista actualizada
        lista = {"tipo": "usuarios", "sala": sala, "lista": usuarios[sala]} # Lista actualizada de usuarios en la sala
        enviar_mensaje(lista)