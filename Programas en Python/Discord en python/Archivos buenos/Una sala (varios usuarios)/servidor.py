import socket, struct, json

MULTICAST_GRP, PORT = ("224.1.1.1", 5007)

usuarios = {} # Diccionario para la lista de usuarios por sala

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', PORT))

grupo = socket.inet_aton(MULTICAST_GRP)
mreq = struct.pack('4sL', grupo, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print("Servidor de chat multicast activo...")

while (True):
    data, adr = sock.recvfrom(1024)
    msg = json.loads(data.decode())

    if (msg["tipo"] == "inicio"):
        sala = msg["sala"]
        user = msg["user"]

        usuarios.setdefault(sala, [])

        if (user not in usuarios[sala]):
            usuarios[sala].append(user)

        # Retransmitir lista de usuarios
        lista = {"tipo": "usuarios", "sala": sala, "lista": usuarios[sala]}
        sock.sendto(json.dumps(lista).encode(), (MULTICAST_GRP, PORT))