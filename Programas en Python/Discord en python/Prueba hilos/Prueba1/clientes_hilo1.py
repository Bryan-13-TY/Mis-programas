import socket
import threading

def recibir_mensajes(sock, detener_evento):
    while not detener_evento.is_set():
        try:
            mensaje, _ = sock.recvfrom(1024)
            if mensaje:
                print("\nMensaje recibido: " + mensaje.decode('utf-8'))
        except:
            break

def enviar_mensajes(sock, servidor, detener_evento):
    while not detener_evento.is_set():
        try:
            mensaje = input("Escribe un mensaje: ")
            if mensaje.lower() == "salir":
                detener_evento.set()
                break
            sock.sendto(mensaje.encode('utf-8'), servidor)
        except:
            break

def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind a puerto fijo local para recibir mensajes
    cliente.bind(("127.0.0.1", 0))  # 0 = puerto asignado automáticamente
    puerto_local = cliente.getsockname()[1]
    print(f"Cliente iniciado en puerto {puerto_local}")
    
    servidor = ("127.0.0.1", 5000)
    print("Conectado al chat UDP. Escribe 'salir' para cerrar.")

    # Evento para detener hilos
    detener_evento = threading.Event()

    # Hilos para enviar y recibir
    hilo_recibir = threading.Thread(target=recibir_mensajes, args=(cliente, detener_evento))
    hilo_enviar = threading.Thread(target=enviar_mensajes, args=(cliente, servidor, detener_evento))

    hilo_recibir.start()
    hilo_enviar.start()

    hilo_enviar.join()
    hilo_recibir.join()

    cliente.close()
    print("Conexión cerrada.")

if __name__ == "__main__":
    main()