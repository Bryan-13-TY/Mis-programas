import socket, json, threading

RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

HOST, PORT = "0.0.0.0", 5007
usuarios = {"general": {}}  # Diccionario: sala → {usuario: (ip, puerto)}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print("Servidor de chat unicast activo...\n")

def enviar_unicast(data: dict, addr: tuple) -> None:
    """Envía un mensaje a un cliente específico."""
    sock.sendto(json.dumps(data).encode(), addr)

def enviar_publico(data: dict, sala: str) -> None:
    """Envía un mensaje a todos los usuarios de la sala."""
    for user_addr in usuarios[sala].values():
        enviar_unicast(data, user_addr)

def manejar_cliente() -> None:
    """Loop principal del servidor."""
    while True:
        data, addr = sock.recvfrom(4096)
        try:
            msj = json.loads(data.decode())
        except:
            continue

        tipo = msj.get("tipo")
        user = msj.get("user")
        sala = msj.get("sala", "general")

        # 1️⃣ Petición de lista de salas
        if tipo == "listar_salas":
            lista = list(usuarios.keys())
            respuesta = {"tipo": "salas", "lista": lista}
            enviar_unicast(respuesta, addr)
            continue

        # Crear sala si no existe
        if sala not in usuarios:
            usuarios[sala] = {}

        # 2️⃣ Usuario entra a la sala
        if tipo == "inicio":
            if user not in usuarios[sala]:
                usuarios[sala][user] = addr
                aviso = {"tipo": "aviso", "sala": sala,
                         "content": f"{GREEN}[+]{RESET}{BLUE}[{user}]{RESET} se ha unido a la sala"}
                enviar_publico(aviso, sala)

            lista = {"tipo": "usuarios", "sala": sala, "lista": list(usuarios[sala].keys())}
            enviar_publico(lista, sala)

        # 3️⃣ Mensaje público
        elif tipo == "msj" and not msj.get("privado", False):
            enviar_publico(msj, sala)

        # 4️⃣ Mensaje privado
        elif tipo == "msj" and msj.get("privado", False):
            destino = msj.get("to")
            if destino in usuarios[sala]:
                enviar_unicast(msj, usuarios[sala][destino])
            else:
                error = {"tipo": "aviso", "sala": sala,
                         "content": f"[Sistema] Usuario '{destino}' no está conectado."}
                enviar_unicast(error, addr)

        # 5️⃣ Usuario sale
        elif tipo == "salir":
            if user in usuarios[sala]:
                usuarios[sala].pop(user)
                aviso = {"tipo": "aviso", "sala": sala,
                         "content": f"{RED}[-]{RESET}{BLUE}[{user}]{RESET} ha abandonado la sala"}
                enviar_publico(aviso, sala)

            lista = {"tipo": "usuarios", "sala": sala, "lista": list(usuarios[sala].keys())}
            enviar_publico(lista, sala)

        # 6️⃣ Usuario envía audio
        elif tipo == "audio":
            aviso = {"tipo": "aviso", "sala": sala,
                     "content": f"{GREEN}[🎙️][{user}]{RESET} ha enviado un audio"}
            enviar_publico(aviso, sala)

def main() -> None:
    threading.Thread(target=manejar_cliente, daemon=True).start()
    print("Esperando mensajes...")
    while True:
        pass

if __name__ == "__main__":
    main()