import socket, struct, json, time

MULTICAST_GRP, PORT = ("224.1.1.1", 5007)

# Diccionario de usuarios: {"general": {"usuario": (IP, puerto)}}
usuarios = {"general": {}}

# Socket UDP para recibir mensajes de clientes
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', PORT))

# Socket UDP multicast para enviar mensajes públicos
sock_multicast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

print("Servidor de chat multicast activo...")

def enviar_multicast(data: dict):
    sock_multicast.sendto(json.dumps(data).encode(), (MULTICAST_GRP, PORT))

def enviar_unicast(data: dict, addr: tuple):
    sock.sendto(json.dumps(data).encode(), addr)

while True:
    data, addr = sock.recvfrom(1024)
    msj = json.loads(data.decode())
    tipo = msj.get("tipo")
    user = msj.get("user")
    sala = msj.get("sala", "general")

    # Usuario se une
    if tipo == "inicio":
        if user not in usuarios[sala]:
            usuarios[sala][user] = addr
            time.sleep(0.05)  # Pequeño retraso

            # Aviso de entrada
            aviso = {"tipo": "aviso", "sala": sala, "content": f"[+][{user}] se ha unido a la sala"}
            enviar_multicast(aviso)

        # Lista de usuarios
        lista = {"tipo": "usuarios", "sala": sala, "lista": list(usuarios[sala].keys())}
        enviar_multicast(lista)

    # Mensaje público
    elif tipo == "msj" and not msj.get("privado", False):
        enviar_multicast(msj)

    # Mensaje privado
    elif tipo == "msj" and msj.get("privado", False):
        destino = msj.get("to")
        if destino in usuarios[sala]:
            enviar_unicast(msj, usuarios[sala][destino])
        else:
            error = {"tipo": "aviso", "sala": sala,
                     "content": f"[Sistema] El usuario '{destino}' no está conectado."}
            enviar_unicast(error, addr)

    # Usuario sale
    elif tipo == "salir":
        if user in usuarios[sala]:
            usuarios[sala].pop(user)
            aviso = {"tipo": "aviso", "sala": sala, "content": f"[-][{user}] ha abandonado la sala"}
            enviar_multicast(aviso)

        lista = {"tipo": "usuarios", "sala": sala, "lista": list(usuarios[sala].keys())}
        enviar_multicast(lista)