import sounddevice as sd
import wavio
from datetime import datetime
from pathlib import Path

# Ruta
carpetaScript = Path(__file__).parent
fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
rutaAudio = carpetaScript/".."/"audio"/f"grabacion_{fecha}.wav"

# Crear carpeta si no existe
rutaAudio.parent.mkdir(parents=True, exist_ok=True)

# Parámetros
duracion = 5 # Segundos 
frecuencia = 44100 # Hz (calidad estándar de audio)

print("Grabando... Habla ahora")
audio = sd.rec(int(duracion * frecuencia), samplerate=frecuencia, channels=2)
sd.wait() # Esperar a que termine la grabación
print("Grabación completa")

# Guardar el archivo
wavio.write(str(rutaAudio), audio, frecuencia, sampwidth=2)
print(f"Audio guardado como '{rutaAudio}'")

# Reproducir el audio grabado
print("Reproduciendo...")
sd.play(audio, frecuencia)
sd.wait()
print("Reproducción terminada")