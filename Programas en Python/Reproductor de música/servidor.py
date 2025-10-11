import socket
import random

HOST = "127.0.0.1"
PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

expected_seq = 0

print("Servidor listo para recibir...")

while True:
    data, addr = sock.recvfrom(1024)
    msg = data.decode()

    if msg == "FIN":
        print("Transmisión terminada.")
        break

    seq = int(msg.split(":")[0])
    contenido = msg.split(":")[1]

    # Simulamos pérdida aleatoria (por ejemplo, 20% de paquetes)
    if random.random() < 0.2:
        print(f"[X] Paquete {seq} perdido (simulado)")
        continue

    print(f"[✔] Recibido paquete {seq}: {contenido}")

    if seq == expected_seq:
        expected_seq += 1
    # ACK acumulativo: siempre el último recibido en orden
    sock.sendto(str(expected_seq).encode(), addr)
