import socket

clientes = set()

def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind(("127.0.0.1", 5000))

    print("Servidor UDP escuchando en 127.0.0.1:5000")

    while True:
        mensaje, addr = servidor.recvfrom(1024)

        # Registrar cliente si es nuevo
        clientes.add(addr)
        print("Cliente conectado desde:", addr)
        print("Mensaje del cliente: ", mensaje.decode('utf-8'))
        print("Lista de clientes: ", clientes)
        

        # Reenviar a todos los demás
        for cliente in clientes:
            if cliente != addr:
                servidor.sendto(mensaje, cliente)

if __name__ == "__main__":
    main()