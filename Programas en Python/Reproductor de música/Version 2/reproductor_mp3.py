import pygame
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

# Inicializar pygame mixer
pygame.mixer.init()

def cargarArchivo():
    global archivo

    archivo = filedialog.askopenfilename(
        title = "Seleccionar archivo MP3",
        filetypes = (("Archivos MP3", "*.mp3"), ("Todos los archivos", "*.*"))
    )

    if archivo:
        pygame.mixer.music.load(archivo)
        etiqueta.config(text = f"Archivo cargado:\n{archivo.split('/')[-1]}")
        btn_play.config(state = "normal")


def reproducir():
    pygame.mixer.music.play()
    etiqueta_estado.config(text = "Reproduciendo...")

def pausar():
    pygame.mixer.music.pause()
    etiqueta_estado.config(text = "Pausado")

def continuar():
    pygame.mixer.music.unpause()
    etiqueta_estado.config(text = "Continuando...")

def detener():
    pygame.mixer.music.stop()
    etiqueta_estado.config(text = "Detenido")

def ajustarVolumen(valor):
    volumen = float(valor)

    pygame.mixer.music.set_volume(volumen)
    etiqueta_volumen.config(text = f"Volumen: {int(volumen * 100)}%")

ventana = tk.Tk()
ventana.title("Reproductor MP3 con Pygame")
ventana.geometry("400x350")
ventana.resizable(False, False)

# Etiquetas
etiqueta = tk.Label(ventana, text = "Ningún archivo cargado", wraplength = 380)
etiqueta.pack(pady = 10)

etiqueta_estado = tk.Label(ventana, text =  "Inactivo", fg = "gray")
etiqueta_estado.pack(pady = 5)

# Botones
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady = 15)

btn_cargar = tk.Button(frame_botones, text = "Cargar MP3", command = cargarArchivo)
btn_cargar.grid(row = 0, column = 0, padx = 5)

btn_play = tk.Button(frame_botones, text = "Reproducir", command = reproducir, state = "disabled")
btn_play.grid(row = 0, column = 1, padx = 5)

btn_pausar = tk.Button(frame_botones, text = "Pausar", command = pausar)
btn_pausar.grid(row = 0, column = 2, padx = 5)

btn_continuar = tk.Button(frame_botones, text = "Continuar", command = continuar)
btn_continuar.grid(row = 0, column = 3, padx = 5)

btn_detener = tk.Button(frame_botones, text = "Detener", command = detener)
btn_detener.grid(row = 0, column = 4, padx = 5)

# Control de volumen
etiqueta_volumen = tk.Label(ventana, text = "Volumen: 70%")
etiqueta_volumen.pack(pady = 5)

control_volumen = ttk.Scale(
    ventana,
    from_ = 0,
    to = 1,
    orient = "horizontal",
    value = 0.7,
    command = ajustarVolumen,
    length = 250
)

control_volumen.pack()

# Establecer volumen inicial
pygame.mixer.music.set_volume(0.7)

# Iniciar ventana
ventana.mainloop()