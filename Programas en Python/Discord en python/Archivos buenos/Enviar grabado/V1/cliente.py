import socket, struct, time
import sounddevice as sd
import numpy as np

SERVER = ("127.0.0.1", 5000)
MAX_BYTES_PAQUETE = 1024
ENCABEZADO_FORMAT = "!I"
ENCABEZADO_SIZE = 4


def grabar_audio_memoria(duracion=10, frecuencia=44100, canales=2):
    """Graba el audio y devuelve los bytes en memoria."""
    print("🎤 Grabando... Habla ahora")
    audio = sd.rec(int(duracion * frecuencia), samplerate=frecuencia, channels=canales, dtype='int16')
    sd.wait()
    print("✅ Grabación completa")

    # Convertir el array NumPy a bytes
    audio_bytes = audio.tobytes()
    return audio_bytes, frecuencia, canales


def enviar_audio_gbn(sock: socket.socket, server_addr: tuple, audio_bytes: bytes, frecuencia: int, canales: int, window_size=6):
    """
    Envía el audio en memoria al servidor usando Go-Back-N.
    """
    tamano_archivo = len(audio_bytes)
    total_paquetes = (tamano_archivo + MAX_BYTES_PAQUETE - 1) // MAX_BYTES_PAQUETE

    # Enviar encabezado con información del audio
    meta_datos = f"AUDIOINFO|grabacion.wav|{tamano_archivo}|{total_paquetes}|{frecuencia}|{canales}"
    sock.sendto(meta_datos.encode(), server_addr)

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

        # Esperar ACK
        try:
            data, _ = sock.recvfrom(4096)
            if data.startswith(b"ACK"):
                ACK_seq = struct.unpack(ENCABEZADO_FORMAT, data[3:3+ENCABEZADO_SIZE])[0]
                if ACK_seq >= first_num_seq_ACKed:
                    first_num_seq_ACKed = ACK_seq + 1
                    print(f">> Confirmado ACK{ACK_seq}")
        except socket.timeout:
            print(f">> Timeout, reenvío desde paquete {first_num_seq_ACKed}")
            sgt_num_seq = first_num_seq_ACKed
            continue

    sock.sendto(b"FIN", server_addr)
    print("✅ Audio enviado completamente.")


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", 0))

    # Grabar audio y enviar directamente
    audio_bytes, frecuencia, canales = grabar_audio_memoria(duracion=5)
    enviar_audio_gbn(sock, SERVER, audio_bytes, frecuencia, canales)

    sock.close()


if __name__ == "__main__":
    main()