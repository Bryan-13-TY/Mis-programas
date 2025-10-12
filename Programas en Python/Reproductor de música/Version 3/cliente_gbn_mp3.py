import socket, struct, tempfile
from pathlib import Path
from reproductor import interfazReproductor # Se importa el reproductor

SERVER = ("127.0.0.1", 5000) # Dirección IP y puerto del servidor
PACKET_PAYLOAD = 1024 # Tamaño en bytes del contenido útil dentro de cada paquete
HEADER_FMT = "!I" # Se usa para convertir 'seq' a 'bytes'
HEADER_SIZE = 4 # Tamaño en bytes del header

def pedirLista(sock):
    sock.sendto(b"LIST", SERVER) # Se envía el mensaje al servidor para perdir la lista
    data, _ = sock.recvfrom(65536) # Espera la respuesta (tamaño máximo)
    songs = data.decode().split("::") if data else [] # Se convierte a una lista
    
    return [s for s in songs if s] # Devuelve la lista final

def recibeArchivo_GBN(sock: socket.socket, song_name: str, timeout=2.0, window_size=6):
    # Pedir archivo
    sock.sendto(f"GET:{song_name}".encode(), SERVER) # Solicita la canción al servidor

    # Primero esperar FILEINFO o ERROR
    sock.settimeout(5.0)
    
    try: # Intenta obtener respuesta del sevidor
        data, _ = sock.recvfrom(65536)
    except socket.timeout:
        raise RuntimeError("No hubo respuesta del servidor (TIMEOUT).")

    header = data.decode(errors="ignore")

    if header.startswith("ERROR"):
        raise RuntimeError("Servidor respondió error: " + header)

    if not header.startswith("FILEINFO"):
        raise RuntimeError("Respuesta inesperada: " + header)

    # Parsear FILEINFO|name|filesize|total_packets
    parts = header.split("|")
    _, fname, filesize_s, total_packets_s = parts
    filesize = int(filesize_s)
    total_packets = int(total_packets_s)
    
    print(f"Recibiendo '{fname}' ({filesize} bytes) en {total_packets} paquetes.")

    # Preparar buffer para paquetes
    received = {} # seq -> bytes (Diccionario para guardar los fragmentos recibidos indexados por número de secuencia)
    expected = 0 # Número de secuencia que el cliente espera recibir
    
    sock.settimeout(timeout) # 2s para menejar reenvios
    last_ack_sent = -1

    # Bucle donde se reciben los paquetes del servidor
    while expected < total_packets:
        try: # Se intenta leer un paquete bloqueante
            pkt, _ = sock.recvfrom(4096)
        except socket.timeout:
            # Timeout: reenviar ACK del último recibido (GBN: cliente solo reenvía ACK del último recibido)
            ack_seq = expected - 1 # Indica cual es la última posición confirmada
            
            if ack_seq >= 0:
                ack_packet = b"ACK" + struct.pack(HEADER_FMT, ack_seq)
                sock.sendto(ack_packet, SERVER)
            
            print(f"Cliente timeout, reenviando ACK{ack_seq}")
            
            continue

        if pkt == b"FIN": # Rompe la señal de fin enviada por el servidor
            break

        # Extraer seq
        if len(pkt) < HEADER_SIZE: # Verifica el tamaño minimo del paquete
            continue
        
        seq = struct.unpack(HEADER_FMT, pkt[:HEADER_SIZE])[0] # Extrae 'seq' del 'header'
        payload = pkt[HEADER_SIZE:] # Extrae 'payload' a partir de 'HEADER_SIZE'

        # Lógica de acetación del paquete
        if seq == expected: # Paquete esperado
            # Aceptar y avanzar cuantos sigan en buffer consecutivos
            received[seq] = payload

            # Consumir en orden
            while expected in received:
                expected += 1
            
            # Enviar ACK acumulativo (expected - 1)
            ack_to_send = expected - 1
            ack_packet = b"ACK" + struct.pack(HEADER_FMT, ack_to_send)
            sock.sendto(ack_packet, SERVER)
            
            last_ack_sent = ack_to_send
            # print(f"Recibido y ACK {ack_to_send}")
        elif seq > expected: # Paquete fuera de orden
            # Paquete fuera de orden: guardar para posible futuro
            if seq not in received:
                received[seq] = payload
            
            # Reenviar último ACK válido
            ack_seq = expected - 1
            
            if ack_seq >= 0:
                ack_packet = b"ACK" + struct.pack(HEADER_FMT, ack_seq)
                sock.sendto(ack_packet, SERVER)
        else: # Paquete duplicado
            # seq < expected -> paquete duplicado, reenviar ACK
            ack_packet = b"ACK" + struct.pack(HEADER_FMT, seq)
            sock.sendto(ack_packet, SERVER)

    # Ensamblar bytes en orden (se ensambla el archivo y se almcena temporalmente)
    file_bytes = bytearray() 

    for i in range(total_packets): # Se concatenan en orden los chuncks desde 0 hasta total_packets 
        chunk = received.get(i, b"")
        file_bytes.extend(chunk)

    file_bytes = file_bytes[:filesize]  # Recortar exceso (último chunk)

    # Guardar en archivo temporal (persistente hasta que lo borres)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix="." + Path(fname).suffix.lstrip("."))
    tmp.write(file_bytes)
    tmp.flush()
    tmp_path = tmp.name
    tmp.close()
    print(f"Archivo guardado temporalmente en: {tmp_path}")

    return tmp_path # Devuelve la ruta del archivo temporal

def main():
    # Se crea el socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", 0))  # Se liga al socket al puerto efímero local
    sock.settimeout(5.0)

    print("Solicitando lista de canciones al servidor...")
    songs = pedirLista(sock) # Se obtiene la lista de canciones
    
    if not songs: # Si no hay canciones
        print("No hay canciones disponibles o no se pudo obtener la lista.")
        return

    for idx, s in enumerate(songs, start=1): # Se imprimen y se enumeran las canciones
        print(f"{idx}. {s}")

    choice = input("Elige el número de la canción a reproducir: ").strip() # Se pide la canción

    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(songs):
        print("Opción inválida.")
        
        return

    song = songs[int(choice) - 1] # Canción elegida
    print(f"Solicitando '{song}'...")

    try: # Se trata de obtener la ruta de la canción
        tmp_path = recibeArchivo_GBN(sock, song)
    except Exception as e:
        print("Error recibiendo archivo:", e)
        return

    # Llamar a tu interfaz para reproducir (usa ruta temporal)
    interfazReproductor(tmp_path)
    print("Reproducción iniciada (archivo temporal).")

if __name__ == "__main__":
    main()