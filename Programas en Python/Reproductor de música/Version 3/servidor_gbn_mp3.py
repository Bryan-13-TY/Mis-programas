import socket, struct
from pathlib import Path

SERVER_ADDR = ("0.0.0.0", 5000) # IP y puerto donde escucha el servidor ('0.0.0.0' -> Todas las interfaces)
PACKET_PAYLOAD = 1024 # Tamaño en bytes del contenido útil dentro de cada paquete
HEADER_FMT = "!I" # Se usa para convertir 'seq' a 'bytes'
HEADER_SIZE = 4 # Tamaño en bytes del header
TIMEOUT = 0.5 # No se usa (quitar)

def listarCanciones() -> list[str]:
    """
    Obtiene los nombres de las canciones en la carpeta 'pistas' y los guarda en una lista.
    
    Es la respuesta a la petición 'LIST' del cliente.

    Returns
    -------
    list[str]
        Lista de los nombres de las canciones en la carpeta 'pistas'.
    """
    carpetaCanciones = Path(__file__).parent/"pistas" # Construir la ruta a la carpeta de las canciones

    if (not carpetaCanciones.exists()):
        return [] # Devuelve una lista vacía si no hay canciones
    
    listaCanciones = [f.name for f in carpetaCanciones.glob("*.mp3")] # Guarda los nombres de las canciones en la lista

    return listaCanciones # Devuelve solo los nombres de las canciones

def enviarArchivo_GBN(sock: socket.socket, clientAddr: tuple, filepath: Path, window_size = 6) -> None:
    """
    Envía el archivo .mp3 usando Go-Back-N.

    Formato del paquete: [4 bytes seq][payload bytes]
    ACK: b"ACK" + bytes seq.

    Parameters
    ----------
    sock : socket.soscket
        Socket UDP ya creado y enlazado.
    clienteAddr : tuple
        Tupla (ip, puerto) del cliente destino.
    filepath : Path
        Path del archivo .mp3 a enviar.
    window_size : int
        Número máximo de paquetes "en vuelo" (tamaño de la ventana GBN).
    """
    filesize = filepath.stat().st_size # Se calcula el tamaño del archivo mp3
    total_packets = (filesize + PACKET_PAYLOAD - 1) // PACKET_PAYLOAD # Se calcula el tamaño del paquete

    # Leer todo el archivo en memoria
    with open(filepath, "rb") as file:
        file_bytes = file.read()

    print(f"\n>> Se envia al cliente: '{filepath.name}' ({filesize} bytes) en {total_packets} paquetes a {clientAddr}")

    base = 0 # Primer paquete no confirmado
    next_seq = 0 # Siquiente número de secuencia que no se ha enviado todavía

    sock.settimeout(1.0) # Para recibir ACKs con timeout (al expirar el servidor retransmite)

    # Primer mensaje: enviar tamaño y número total de paquetes (informativo)
    mensajeInicial = f"FILEINFO|{filepath.name}|{filesize}|{total_packets}"
    sock.sendto(mensajeInicial.encode(), clientAddr)

    # Bucle principal para el envió Go-Back-N
    while (base < total_packets):
        # Enviar paquetes dentro de la ventana
        while ((next_seq < base + window_size) and (next_seq < total_packets)): # Envía tantos paquetes como permita la ventana
            # Para cada next_seq se calcula lo siguiente:
            start = next_seq * PACKET_PAYLOAD
            end = start + PACKET_PAYLOAD
            payload = file_bytes[start:end]
            header = struct.pack(HEADER_FMT, next_seq) # Se empaqueta next_seq
            packet = header + payload

            sock.sendto(packet, clientAddr) # Se envía el paquete al cliente
            print(f"Sent pkt {next_seq}")
            next_seq += 1

        # Esperamos ACK
        try:
            data, addr = sock.recvfrom(4096)
            
            if (addr != clientAddr): # Si la dirección del mensaje es diferente con la del cliente
                # Ignorar otros clientes en este (evitar mezclar clientes)
                continue

            if (data.startswith(b"ACK")): # Si el paquete empieza con b"ACK"
                ack_seq = struct.unpack(HEADER_FMT, data[3:3 + HEADER_SIZE])[0] # Se extrae los 4 bytes siguientes como número de secuencia
                
                # ACK acumulativo: mueve la base
                if (ack_seq >= base):
                    base = ack_seq + 1
                    print(f"ACK {ack_seq} -> base={base}")
            elif (data.startswith(b"STOP")): # Si el paquete empieza con b"STOP"
                print("Cliente solicitó detener la transferencia") 

                return
        except sock.timeout: # Si recvfrom excede 1 segundo
            # Se considera la perdida de ACK, reenviar desde base (Go-Back-N)
            print(f"Timeout en servidor: Reenviando desde paquete {base}")

            next_seq = base # Retroceder

    # Se envía la confirmación (todos los paquetes confirmados)
    sock.sendto(b"FIN", clientAddr) # Confirmación del termino de la transferencia

    print("Transferencia completada")

def main():
    # Se crea y bindea un socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(SERVER_ADDR)

    print(f">> Servidor GBN MP3 escuchando en {SERVER_ADDR}")

    while (True):
        data, addr = sock.recvfrom(4096)
        mensaje = data.decode(errors="ignore")

        if (mensaje == "LIST"): # Cliente solicita la lista de canciones
            listaCanciones = listarCanciones()
            payload = "::".join(listaCanciones)
            sock.sendto(payload.encode(), addr)
            print(f">> Lista enviada a {addr} ({len(listaCanciones)} canciones)")
        elif (mensaje.startswith("GET:")):
            song_name = mensaje.split(":", 1)[1]
            path = Path(__file__).parent/"pistas"/song_name

            if (not path.exists()):
                sock.sendto(b"ERROR|NOFILE", addr)

                print(f"Cliente pidió '{song_name}' pero no existe.")

                continue

            # Enviar archivo con GBN
            enviarArchivo_GBN(sock, addr, path, window_size = 6)
        else:
            # Mensaje desconocido
            sock.sendto(b"ERROR|UNKNOWN", addr)

if __name__ == "__main__":
    main()