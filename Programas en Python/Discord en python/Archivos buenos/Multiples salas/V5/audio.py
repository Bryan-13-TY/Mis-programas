"""
Clase 'Audio' para manejar todo lo relacionado al audio del lado del cliente.

Se cuentan con los métodos para grabar un audio, buscarlo y reproducirlo al
encontrarlo. 

Autores:
    - García Escamilla Bryan Alexis
    - Meléndez Macedonio Rodrigo

Fecha: 08/11/2025
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from pathlib import Path

import pygame
import sounddevice as sd
import wavio

import utils as utl

pygame.mixer.init() # inicializamos el reproductor

class Audio:
    def grabar_audio(self, mensaje: dict, script: Path, sala: str, usuario: str) -> str:
        """
        Método para grabar un audio, reproducirlo y posteriormente guardarlo.

        Parameters
        ----------
        mensaje : dict
            Diccionario con los metadatos para la grabación.
        script : Path
            Ruta donde se encuentra el script cliente.py.
        sala : str
            Nombre de la sala desde donde se graba el audio.
        usuario: str
            Nombre del usuario que graba el audio.

        Returns
        -------
        str
            Nombre asignado a la grabación.
        """
        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        if mensaje.get("privado"): # es un mensaje privado
            dest = mensaje.get("to")
            grabacion = script / f"{sala}" / f"{dest}" / f"{usuario}_{fecha}.wav"
        else: # es un mensaje público
            grabacion = script / f"{sala}" / f"{usuario}_{fecha}.wav"

        duracion, frecuencia = 5, 44100

        print(f">> {utl.RED}[system]{utl.RESET} Grabando audio...")
        audio = sd.rec(int(duracion * frecuencia), samplerate=frecuencia, channels=2)
        sd.wait()
        print(f">> {utl.RED}[system]{utl.RESET} Grabación completa")
        wavio.write(str(grabacion), audio, frecuencia, sampwidth=2) # para guardar el audio grabado
        nombre_audio = str(grabacion).split("\\")[-1]

        return nombre_audio

    def buscar_audio(self, carpeta_sala: Path, carpeta_personal: Path, usuario: str, nombre_audio: str) -> Path | None:
        """
        Método para buscar el audio que se quiere reproducir.

        Parameters
        ----------
        carpeta_sala : Path
            Ruta hacia la carpeta de la sala desde donde se quiere reprodir el audio.
        carpeta_personal : Path
            Ruta hacia la carpeta del usuario que quiere reproducir el audio.
        usuario : str
            Nombre del usuario.
        nombre_audio : str
            Nombre del audio que se quiere buscar.

        Returns
        -------
        Path | None
            Ruta hacia el audio si este existe, de lo contrario None.
        """
        ruta_directa = carpeta_sala / nombre_audio
        if ruta_directa.exists(): # si es un audio público
            return ruta_directa
        
        for archivo in carpeta_sala.rglob("*"): # Si el archivo es privado
            if archivo.is_file:
                nombre = archivo.name
                if nombre.startswith(usuario) and nombre.endswith(nombre_audio):
                    return archivo
        
        ruta_personal = carpeta_personal / nombre_audio
        if ruta_personal.exists(): # si el archivo es privado
            return ruta_personal

        return None
    
    def reproducir_audio(self, ruta_audio: Path, nombre_audio: str) -> None:
        """
        Método para controlar la reproducción del audio.

        Parameters
        ----------
        ruta_audio : Path
            Ruta hacia el audio a reproducir.
        nombre_audio : str
            Nombre del audio que se quiere reproducir.
        """
        def reproducir() -> None:
            """Comienza la reproducción del audio al presionar el botón 'Reproducir'."""
            pygame.mixer.music.play()
            label_state.config(text="Reproduciendo audio...")
    
        def pausar() -> None:
            """Pausa la reproducción del audio al presionar el botón 'Pausar'."""
            pygame.mixer.music.pause()
            label_state.config(text="Audio en pausa")

        def continuar() -> None:
            """Continua la reproducción del audio al presionar el botón 'Coninuar'."""
            pygame.mixer.music.unpause()
            label_state.config(text="Continuando audio...")

        def detener() -> None:
            """Detiene la reproducción del audio al presionar el botón 'Detener'."""
            pygame.mixer.music.stop()
            label_state.config(text="Audio detenido")

        def ajustar_volumen(valor: int) -> None:
            """
            Ajusta el volumen del audio.

            Parameters
            ----------
            valor : int
                Volumen inicial del audio.
            """
            volumen = float(valor)

            pygame.mixer.music.set_volume(volumen)
            label_volume.config(text=f"Volumen al {int(volumen * 100)}%")

        try:
            pygame.mixer.music.load(ruta_audio)
            archivo_cargado = True
        except Exception as e:
            archivo_cargado = False
            print(f"Error al cargar el archivo: {e}")

        # se crea la ventana
        root = tk.Tk()
        root.title("Reproductor")
        root.geometry("400x300")
        root.resizable(False, False)

        if archivo_cargado:
            label = tk.Label(root, text=f"Audio cargado: \n{nombre_audio}", wraplength=380)
        else:
            label = tk.Label(root, text="No se pudo cargar el audio", fg="red")

        label.pack(pady=10)
        label_state = tk.Label(root, text="Reproductor inactivo", fg="gray")
        label_state.pack(pady=5)

        # se crean los botones
        frame_btns = tk.Frame(root)
        frame_btns.pack(pady=15)

        btn_play = tk.Button(frame_btns, text="▶️ Reproducir", command=reproducir, state="normal" if archivo_cargado else "disabled")
        btn_play.grid(row=0, column=0, padx=5)
        btn_pause = tk.Button(frame_btns, text="⏸️ Pausar", command=pausar, state="normal" if archivo_cargado else "disabled")
        btn_pause.grid(row=0, column=1, padx=5)
        btn_continue = tk.Button(frame_btns, text="▶️ Continuar", command=continuar, state="normal" if archivo_cargado else "disabled")
        btn_continue.grid(row=0, column=2, padx=5)
        btn_stop = tk.Button(frame_btns, text="⏹️ Detener", command=detener, state="normal" if archivo_cargado else "disabled")
        btn_stop.grid(row=0, column=3, padx=5)

        # se crea el label para el volumen del audio
        label_volume = tk.Label(root, text="Volumen al 50%")
        label_volume.pack(pady=5)

        control_volume = ttk.Scale(root, from_=0, to=1, orient="horizontal", value=0.5, command=ajustar_volumen, length=250) # type: ignore
        control_volume.pack()
        pygame.mixer.music.set_volume(0.5)

        root.mainloop()