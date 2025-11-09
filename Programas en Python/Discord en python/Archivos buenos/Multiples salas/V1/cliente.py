import socket, threading, json, sys, sounddevice as sd, wavio
from datetime import datetime
from pathlib import Path

SERVER_IP, SERVER_PORT = "127.0.0.1", 5007

YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
ORANGE = "\033[33m"
RESET = "\033[0m"

class ChatCliente:
    def __init__(self, usuario: str, sala: str) -> None:
        self.usuario = usuario
        self.sala = sala
        self.activo = True

        # Socket UDP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', 0))

        # Avisar al servidor que entra el usuario
        inicio = {"tipo": "inicio", "user": self.usuario, "sala": self.sala}
        self.sock.sendto(json.dumps(inicio).encode(), (SERVER_IP, SERVER_PORT))

    def grabar_audio(self) -> None:
        """Graba audio, lo reproduce y lo guarda en la carpeta de la sala."""
        carpeta_script = Path(__file__).parent
        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        ruta = carpeta_script / f"{self.sala}" / f"grabacion_{self.usuario}_{fecha}.wav"
        ruta.parent.mkdir(parents=True, exist_ok=True)

        duracion, frecuencia = (10, 44100)
        print("Grabando audio...")
        audio = sd.rec(int(duracion * frecuencia), samplerate=frecuencia, channels=2)
        sd.wait()
        print("Grabación completa. Reproduciendo...")
        sd.play(audio, frecuencia)
        sd.wait()
        print("Reproducción terminada.")
        wavio.write(str(ruta), audio, frecuencia, sampwidth=2)

    def recibir(self) -> None:
        """Recibe mensajes del servidor."""
        while self.activo:
            try:
                data, _ = self.sock.recvfrom(4096)
                msj = json.loads(data.decode())
                sala_msg = msj.get("sala", self.sala)
                if sala_msg != self.sala:
                    continue

                if msj["tipo"] == "msj":
                    if msj.get("privado"):
                        print(f"{YELLOW}[Privado de {msj['from']}]{RESET}: {msj['content']}")
                    else:
                        print(f"{BLUE}[{msj['user']}]{RESET}: {msj['content']}")
                elif msj["tipo"] == "aviso":
                    print(msj["content"])
                elif msj["tipo"] == "usuarios":
                    print(f"\nUsuarios en sala {MAGENTA}'{self.sala}'{RESET}: "
                          f"{MAGENTA}{', '.join(msj['lista'])}{RESET}\n")
            except:
                break

    def enviar(self) -> None:
        """Envia mensajes o comandos al servidor."""
        while self.activo:
            try:
                texto = input("").strip()
                if texto.lower() == "/salir":
                    salir = {"tipo": "salir", "user": self.usuario, "sala": self.sala}
                    self.sock.sendto(json.dumps(salir).encode(), (SERVER_IP, SERVER_PORT))
                    self.activo = False
                    print("Has salido de la sala.")
                    break
                elif texto.lower() == "/audio":
                    audio = {"tipo": "audio", "user": self.usuario, "sala": self.sala}
                    self.grabar_audio()
                    self.sock.sendto(json.dumps(audio).encode(), (SERVER_IP, SERVER_PORT))
                elif texto.startswith("@"):
                    partes = texto.split(" ", 1)
                    if len(partes) < 2:
                        print("Formato: @usuario mensaje")
                        continue
                    destino, contenido = partes
                    destino = destino[1:]
                    mensaje = {"tipo": "msj", "privado": True, "from": self.usuario,
                               "to": destino, "content": contenido, "sala": self.sala}
                    self.sock.sendto(json.dumps(mensaje).encode(), (SERVER_IP, SERVER_PORT))
                    print(f"{ORANGE}[Tú -> {destino}]{RESET}: {contenido}")
                else:
                    mensaje = {"tipo": "msj", "privado": False, "user": self.usuario,
                               "sala": self.sala, "content": texto}
                    self.sock.sendto(json.dumps(mensaje).encode(), (SERVER_IP, SERVER_PORT))
            except KeyboardInterrupt:
                salir = {"tipo": "salir", "user": self.usuario, "sala": self.sala}
                self.sock.sendto(json.dumps(salir).encode(), (SERVER_IP, SERVER_PORT))
                self.activo = False
                sys.exit(0)

    def iniciar(self) -> None:
        threading.Thread(target=self.recibir, daemon=True).start()
        self.enviar()

# --- Selección de sala ---
def obtener_salas() -> list:
    """Solicita la lista de salas al servidor."""
    temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    temp_sock.bind(('', 0))
    peticion = {"tipo": "listar_salas"}
    temp_sock.sendto(json.dumps(peticion).encode(), (SERVER_IP, SERVER_PORT))
    data, _ = temp_sock.recvfrom(4096)
    temp_sock.close()
    try:
        respuesta = json.loads(data.decode())
        return respuesta["lista"] if respuesta["tipo"] == "salas" else []
    except:
        return []

def main() -> None:
    print("Obteniendo salas disponibles...\n")
    salas_disponibles = obtener_salas()

    if salas_disponibles:
        print("Salas disponibles:")
        for i, s in enumerate(salas_disponibles, 1):
            print(f" {i}. {s}")
    else:
        print("No hay salas activas. Se creará una nueva al unirte.\n")

    sala = input("\nEscribe el nombre de la sala a la que deseas unirte (o crea una nueva): ").strip()
    if not sala:
        sala = "general"

    usuario = input("Ingresa tu nombre de usuario: ")
    cliente = ChatCliente(usuario, sala)
    cliente.iniciar()

if __name__ == "__main__":
    main()