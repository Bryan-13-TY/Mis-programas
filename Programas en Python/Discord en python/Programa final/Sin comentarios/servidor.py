import socket
import json
import threading
import struct
import time
from pathlib import Path

import wave

import utils

SERVER_ADDR = ("0.0.0.0", 5007)
usuarios = {"general": {}}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(SERVER_ADDR)

print("Servidor de chat activo...")

ENCABEZADO_FORMAT = "!I"
ENCABEZADO_SIZE = 4
MAX_BYTES_PAQUETE = 1024

def enviar_unicast(data: dict, addr: tuple) -> None:
    sock.sendto(json.dumps(data).encode(), addr)


def enviar_publico(data: dict, sala: str) -> None:
    for usuario_addr in usuarios[sala].values():
        enviar_unicast(data, usuario_addr)


def recibir_audio_gbn(audio_sock: socket.socket, cliente_addr: tuple, info: dict) -> None:
    nombre = info.get("nombre", f"{info.get('user','anon')}_{int(time.time())}.wav")
    tamano = int(info.get("tamano", 0))
    total_paquetes = int(info.get("total_paquetes", 0))
    frecuencia = int(info.get("frecuencia", 44100))
    canales = int(info.get("canales", 2))
    sala = info.get("sala", "general")
    privado = bool(info.get("privado", False))
    usuario = info.get("user") or info.get("from") or "anon"
    destinatario = info.get("to")

    print(f">> Iniciando recepción de audio '{nombre}' desde {cliente_addr} (sala='{sala}', user='{usuario}', privado={privado}, paquetes={total_paquetes})")
    paquetes = {}
    num_seq_esperado = 0
    audio_sock.settimeout(3.0)

    while True:
        try:
            paquete, addr = audio_sock.recvfrom(4096)
        except socket.timeout:
            continue

        if 'addr_audio' not in locals():
            addr_audio = addr

        if addr != addr_audio:
            continue

        if paquete == b"FIN":
            print("FIN recibido para transferencia de audio.")
            audio_sock.settimeout(None)
            break

        if len(paquete) < ENCABEZADO_SIZE:
            continue

        num_seq = struct.unpack(ENCABEZADO_FORMAT, paquete[:ENCABEZADO_SIZE])[0]
        datos = paquete[ENCABEZADO_SIZE:]

        if num_seq == num_seq_esperado:
            paquetes[num_seq] = datos
            num_seq_esperado += 1

            ack = {"tipo": "ACK",
                   "num_seq": num_seq}
            audio_sock.sendto(json.dumps(ack).encode(), addr_audio)
            print(f">> Recibido paquete {num_seq}, enviado ACK{num_seq}")
        else:
            ack_num = max(0, num_seq_esperado - 1)
            ack = {"tipo": "ACK",
                   "num_seq": ack_num}
            audio_sock.sendto(json.dumps(ack).encode(), addr_audio)
            print(f">> Paquete fuera de orden {num_seq}, reenvío ACK{ack_num}")

    audio_bytes = bytearray()
    for i in range(num_seq_esperado):
        audio_bytes.extend(paquetes.get(i, b""))

    audio_bytes = bytes(audio_bytes[:tamano])

    carpeta = Path(__file__).parent
    carpeta_sala = carpeta / f"{sala}"
    carpeta_sala.mkdir(parents=True, exist_ok=True)

    if privado and destinatario:
        carpeta_dest = carpeta_sala / f"{destinatario}"
        carpeta_dest.mkdir(parents=True, exist_ok=True)
        ruta_archivo = carpeta_dest / nombre
    else:
        ruta_archivo = carpeta_sala / nombre

    try:
        with wave.open(str(ruta_archivo), "wb") as wf:
            wf.setnchannels(canales)
            wf.setsampwidth(2)
            wf.setframerate(frecuencia)
            wf.writeframes(audio_bytes)
        print(f"💾 Audio guardado en: {ruta_archivo}")
    except Exception as e:
        print(f"Error al guardar audio: {e}")
        return
    
    aviso = {"tipo": "audio",
             "sala": sala,
             "from": usuario,
             "nombre": nombre,
             "privado": privado,
             "content": f"{utils.GREEN}[🎙️][{usuario}]{utils.RESET} ha enviado el audio '{nombre}'"}
    
    if privado and destinatario:
        if destinatario in usuarios.get(sala, {}):
            enviar_unicast(aviso, usuarios[sala][destinatario])
        else:
            error = {"tipo": "aviso",
                     "sala": sala,
                     "content": f">> {utils.RED}[system]{utils.RESET} Usuario '{destinatario}' no está conectado"}
            enviar_unicast(error, usuarios[sala].get(usuario, cliente_addr))
    else:
        enviar_publico(aviso, sala)

    try:
        audio_sock.close()
    except:
        pass


def manejar_cliente() -> None:
    while True:
        data, addr = sock.recvfrom(4096)
        try:
            mensaje = json.loads(data.decode())
        except:
            continue

        tipo = mensaje.get("tipo")
        usuario = mensaje.get("user") or mensaje.get("from")
        sala = mensaje.get("sala", "general")

        if tipo == "listar_salas":
            salas = list(usuarios.keys())
            respuesta = {"tipo": "salas",
                         "lista": salas}
            enviar_unicast(respuesta, addr)
            continue

        if sala not in usuarios:
            usuarios[sala] = {}

        if tipo == "inicio":
            if usuario not in usuarios[sala]:
                usuarios[sala][usuario] = addr
                aviso = {"tipo": "aviso",
                         "sala": sala,
                         "content": f">> {utils.GREEN}[+]{utils.RESET}{utils.BLUE}[{usuario}]{utils.RESET} se ha unido a la sala"}
                enviar_publico(aviso, sala)

            usuarios_sala = {"tipo": "usuarios",
                             "sala": sala,
                             "lista": list(usuarios[sala].keys())}
            enviar_publico(usuarios_sala, sala)

        elif tipo == "msj":
            if not mensaje.get("privado", False):
                enviar_publico(mensaje, sala)
            elif mensaje.get("privado", False):
                dest = mensaje.get("to")
                if dest in usuarios[sala]:
                    enviar_unicast(mensaje, usuarios[sala][dest])
                else:
                    error = {"tipo": "aviso",
                             "sala": sala,
                             "content": f">> {utils.RED}[system]{utils.RESET} Usuario '{dest}' no está conectado"}
                    enviar_unicast(error, addr)

        elif tipo == "salir":
            if usuario in usuarios[sala]:
                usuarios[sala].pop(usuario)
                aviso = {"tipo": "aviso",
                         "sala": sala,
                         "content": f">> {utils.RED}[-]{utils.RESET}{utils.BLUE}[{usuario}]{utils.RESET} ha abandonado la sala"}
                enviar_publico(aviso, sala)

            usuarios_sala = {"tipo": "usuarios",
                             "sala": sala,
                             "lista": list(usuarios[sala].keys())}
            enviar_publico(usuarios_sala, sala)

        elif tipo == "AUDIOINFO" or tipo == "audio":
            try:
                audio_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                audio_sock.bind(("0.0.0.0", 0))
                audio_port = audio_sock.getsockname()[1]

                respuesta = {"tipo": "READY",
                             "port": audio_port}
                enviar_unicast(respuesta, addr)

                threading.Thread(target=recibir_audio_gbn, args=(audio_sock, addr, mensaje), daemon=True).start()
            except Exception as e:
                print(f"Error iniciando transferencia de audio: {e}")
                error = {"tipo": "aviso",
                         "sala": sala,
                         "content": f">> {utils.RED}[system]{utils.RESET} No se pudo iniciar transferencia de audio."}
                enviar_unicast(error, addr) 


def main() -> None:
    threading.Thread(target=manejar_cliente, daemon=True).start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print("\nServidor detenido.")
            break

if __name__ == "__main__":
    main()