import os, pygame, msvcrt
from pathlib import Path

def limpiarTerminal() -> None:
    """
    Limpia la terminal de cualquier sistema operativo. 
    """
    os.system('cls' if os .name == 'nt' else 'clear')

def esperarTecla():
    """
    Espera a que se presione cualquier tecla.
    """
    return msvcrt.getch().decode("utf-8")  # devuelve la tecla como string

def obtenerRuta():
    carpetaScript = Path(__file__).parent
    rutaAudio = carpetaScript/"pistas"/"Have You Ever Seen The Rain.mp3"

    return rutaAudio

def mezclador():
    rutaAudio = obtenerRuta()

    pygame.mixer.init() # Inicializamos el mezclador de audio
    pygame.mixer.music.load(rutaAudio) # Cargar el archivo MP3
    pygame.mixer.music.set_volume(0.7) # Establecer volumen (0.0 = silencio, 1.0 = máximo)
    pygame.mixer.music.play()

    print("Reproduciendo....")