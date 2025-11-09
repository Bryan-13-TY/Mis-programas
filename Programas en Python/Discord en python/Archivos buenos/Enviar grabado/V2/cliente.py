import socket, struct, time, json
import sounddevice as sd

SERVER = ("127.0.0.1", 5000)
MAX_BYTES_PAQUETE = 4096
ENCABEZADO_FORMAT = "!I"
ENCABEZADO_SIZE = 4


def grabar_audio_memoria(duracion=5, frecuencia=44100, canales=2):
    print("🎤 Grabando... Habla ahora")
    audio = sd.rec(int(duracion * frecuencia), samplerate=frecuencia, channels=canales, dtype='int16')
    sd.wait()
    print("✅ Grabación completa")
    return audio.tobytes(), frecuencia, canales


def enviar_audio_gbn(sock: socket.socket, server_addr: tuple, audio_bytes: bytes, frecuencia: int, canales: int, window_size=6):
    tamano_archivo = len(audio_bytes)
    total_paquetes = (tamano_archivo + MAX_BYTES_PAQUETE - 1) // MAX_BYTES_PAQUETE

    # Enviar metadatos como JSON
    meta = {
        "tipo": "AUDIOINFO",
        "nombre": "grabacion.wav",
        "tamano": tamano_archivo,
        "total_paquetes": total_paquetes,
        "frecuencia": frecuencia,
        "canales": canales,
    }
    sock.sendto(json.dumps(meta).encode(), server_addr)

    # Esperar confirmación READY
    data, _ = sock.recvfrom(1024)
    if not data:
        print("❌ Sin respuesta del servidor.")
        return

    try:
        msg = json.loads(data.decode())
        if msg.get("tipo") != "READY":
            print("❌ Servidor no listo.")
            return
    except json.JSONDecodeError:
        print("❌ Respuesta inválida del servidor.")
        return

    print(f">> Enviando audio ({tamano_archivo} bytes, {total_paquetes} paquetes)...")

    first_num_seq_ACKed = 0
    sgt_num_seq = 0
    sock.settimeout(2.0)

    while first_num_seq_ACKed < total_paquetes:
        # Enviar paquetes dentro de la ventana
        while sgt_num_seq < first_num_seq_ACKed + window_size and sgt_num_seq < total_paquetes:
            inicio = sgt_num_seq * MAX_BYTES_PAQUETE
            final = inicio + MAX_BYTES_PAQUETE
            chunk = audio_bytes[inicio:final]

            encabezado = struct.pack(ENCABEZADO_FORMAT, sgt_num_seq)
            paquete = encabezado + chunk

            sock.sendto(paquete, server_addr)
            print(f">> Enviado paquete {sgt_num_seq}")
            sgt_num_seq += 1

        try:
            data, _ = sock.recvfrom(4096)
            msg = json.loads(data.decode())
            if msg.get("tipo") == "ACK":
                ACK_seq = msg["num_seq"]
                if ACK_seq >= first_num_seq_ACKed:
                    first_num_seq_ACKed = ACK_seq + 1
                    print(f">> Confirmado ACK{ACK_seq}")

                    # Si ya se confirmó el último paquete, terminamos
                    if first_num_seq_ACKed >= total_paquetes:
                        break
        except (socket.timeout, json.JSONDecodeError):
            print(f">> Timeout, reenvío desde paquete {first_num_seq_ACKed}")
            sgt_num_seq = first_num_seq_ACKed
            continue

    sock.sendto(b"FIN", server_addr)
    print("✅ Audio enviado completamente.")


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", 0))
    audio_bytes, frecuencia, canales = grabar_audio_memoria(duracion=5)
    enviar_audio_gbn(sock, SERVER, audio_bytes, frecuencia, canales)
    sock.close()


if __name__ == "__main__":
    main()