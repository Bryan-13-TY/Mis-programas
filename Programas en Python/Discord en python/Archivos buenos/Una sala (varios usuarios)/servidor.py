import socket, struct, json

MULTICAST_GRP, PORT = ("224.1.1.1", 5007) # Grupo multicast y el puerto
# Las direcciones 224.0.0.0 - 239.255.255.255 son reservadas para multicast

usuarios = {} # Diccionario para la lista de usuarios por sala

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # Creación del socket UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Permite que varios sockets se vinculen al mismo puerto
sock.bind(('', PORT)) # Asocia el socket al puerto 5007 en todas las interfaces de red

# Unirse al grupo multicast
grupo = socket.inet_aton(MULTICAST_GRP) # Convierte la IP multicast a formato binario
mreq = struct.pack('4sL', grupo, socket.INADDR_ANY) # Grupo multicast (4 bytes), cualquier interfaz disponible (entero largo)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq) # Hace que el socket se unaa al grupo multicast, recibiendo los mensajes enviados al grupo 224.1.1.1

print("Servidor de chat multicast activo...")

while (True):
    data, addr = sock.recvfrom(1024) # Espera a recibir un datagrama UDP (1024 bytes)
    msg = json.loads(data.decode()) # Decodifica el mensaje recibido

    if (msg["tipo"] == "inicio"): # Si se trata de un nuevo usuario que se conecta a una sala
        sala = msg["sala"] # Nombre de la sala
        user = msg["user"] # Nombre del usuario qu se conecta a la sala

        usuarios.setdefault(sala, []) # Si la sala no existe en el diccionario, la crea con una lista vacía 

        # Registrar usuario
        if (user not in usuarios[sala]):
            usuarios[sala].append(user) # Agregar usuario a la sala si no existe previamente
            print(f"[+][{user}] se ha unido a la sala [{sala}]")

        # Retransmitir lista de usuarios
        lista = {"tipo": "usuarios", "sala": sala, "lista": usuarios[sala]} # Lista actualizada de usuarios en la sala
        sock.sendto(json.dumps(lista).encode(), (MULTICAST_GRP, PORT)) # Envía la lista al grupo multicast para que todos los clientes reciban la nueva lista