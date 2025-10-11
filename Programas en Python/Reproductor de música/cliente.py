import socket
import time

HOST = "127.0.0.1"
PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2.0)  # Espera máxima por ACK

# Parámetros del algoritmo
window_size = 4
base = 0
next_seq = 0
total_paquetes = 10

# Datos a enviar
paquetes = [f"Paquete-{i}" for i in range(total_paquetes)]

while base < total_paquetes:
    # Enviar todos los que caben en la ventana
    while next_seq < base + window_size and next_seq < total_paquetes:
        msg = f"{next_seq}:{paquetes[next_seq]}"
        sock.sendto(msg.encode(), (HOST, PORT))
        print(f"[→] Enviado {msg}")
        next_seq += 1

    try:
        ack_data, _ = sock.recvfrom(1024)
        ack = int(ack_data.decode())
        print(f"[ACK] Recibido ACK {ack}")

        base = ack  # Mueve la ventana
    except socket.timeout:
        print("[!] Timeout: retransmitiendo desde", base)
        # Retransmitir desde el paquete base
        next_seq = base

# Enviar mensaje final
sock.sendto(b"FIN", (HOST, PORT))
print("Transmisión completada.")
