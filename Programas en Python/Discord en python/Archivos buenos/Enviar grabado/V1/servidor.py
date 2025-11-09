import socket, struct, wave
from pathlib import Path

SERVER_ADDR = ("0.0.0.0", 5000)
MAX_BYTES_PAQUETE = 1024
ENCABEZADO_FORMAT = "!I"
ENCABEZADO_SIZE = 4


def recibir_audio_gbn(sock: socket.socket, cliente_addr: tuple, meta_datos: str, timeout=2.0):
    """
    Recibe un archivo de audio enviado con Go-Back-N y lo guarda como .wav
    """
    _, nombre, tamano_str, total_str, frecuencia_str, canales_str = meta_datos.split("|")
    tamano = int(tamano_str)
    total_paquetes = int(total_str)
    frecuencia = int(frecuencia_str)
    canales = int(canales_str)

    print(f">> Recibiendo audio '{nombre}' de {cliente_addr}")
    print(f"   Tamaño: {tamano} bytes | Paquetes: {total_paquetes} | Frecuencia: {frecuencia} Hz | Canales: {canales}")

    paquetes = {}
    num_seq_esperado = 0
    sock.settimeout(timeout)

    while True:
        try:
            paquete, addr = sock.recvfrom(4096)
        except socket.timeout:
            continue

        if addr != cliente_addr:
            continue

        if paquete == b"FIN":
            print("✅ Fin de transmisión recibido.")
            break

        if len(paquete) < ENCABEZADO_SIZE:
            continue

        num_seq = struct.unpack(ENCABEZADO_FORMAT, paquete[:ENCABEZADO_SIZE])[0]
        datos = paquete[ENCABEZADO_SIZE:]

        if num_seq == num_seq_esperado:
            paquetes[num_seq] = datos
            num_seq_esperado += 1

            ACK = b"ACK" + struct.pack(ENCABEZADO_FORMAT, num_seq)
            sock.sendto(ACK, cliente_addr)
            print(f">> Recibido paquete {num_seq}, enviado ACK{num_seq}")
        else:
            # Reenviar último ACK válido
            ACK = b"ACK" + struct.pack(ENCABEZADO_FORMAT, num_seq_esperado - 1)
            sock.sendto(ACK, cliente_addr)

    # Reconstruir los bytes del audio
    audio_bytes = bytearray()
    for i in range(num_seq_esperado):
        audio_bytes.extend(paquetes.get(i, b""))

    audio_bytes = bytes(audio_bytes[:tamano])

    # Guardar como archivo .wav
    carpeta = Path(__file__).parent / "grabaciones"
    carpeta.mkdir(exist_ok=True)
    ruta_archivo = carpeta / nombre

    with wave.open(str(ruta_archivo), "wb") as wf:
        wf.setnchannels(canales)
        wf.setsampwidth(2)  # 16 bits
        wf.setframerate(frecuencia)
        wf.writeframes(audio_bytes)

    print(f"💾 Audio guardado en: {ruta_archivo}")


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(SERVER_ADDR)

    print(f">> Servidor Go-Back-N escuchando en {SERVER_ADDR}")

    while True:
        data, addr = sock.recvfrom(4096)
        mensaje = data.decode(errors="ignore")

        if mensaje.startswith("AUDIOINFO"):
            sock.sendto(b"READY", addr)
            recibir_audio_gbn(sock, addr, mensaje)
        else:
            sock.sendto(b"ERROR|UNKNOWN", addr)


if __name__ == "__main__":
    main()