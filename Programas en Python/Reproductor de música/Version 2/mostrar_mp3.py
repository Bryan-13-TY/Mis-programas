from pathlib import Path
import os

os.chdir(os.path.dirname(__file__))

rutaPistas = Path("pistas")
canciones = [f.name for f in rutaPistas.glob("*.mp3")]

# print(canciones)

for file in rutaPistas.glob("*.mp3"):
    print(file)

