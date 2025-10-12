import pygame, tkinter as tk, warnings
from tkinter import ttk

warnings.filterwarnings("ignore", category=UserWarning, module="pkg_resources") # Ignoramos las advertencias de la librería
pygame.mixer.init() # Inicializamos pygame mixer

def interfazReproductor(rutaCancion: str) -> None:
    def reproducirCancion() -> None:
        pygame.mixer.music.play()
        label_state.config(text="Reproduciendo...")

    def pausarCancion() -> None:
        pygame.mixer.music.pause()
        label_state.config(text="Pausado")

    def continuarCancion() -> None:
        pygame.mixer.music.unpause()
        label_state.config(text="Continuando...")

    def detenerCancion() -> None:
        pygame.mixer.music.stop()
        label_state.config(text="Detenido")

    def ajustarVolumen(valorInicial: int) -> None:
        volumen = float(valorInicial)

        pygame.mixer.music.set_volume(volumen)
        label_volume.config(text=f"Volumen al {int(volumen * 100)}%")

    try:
        pygame.mixer.music.load(rutaCancion)
        archivoCargado = True
    except Exception as e:
        archivoCargado = False
        print(f"Error al cargar el archivo: {e}")

    ventana = tk.Tk()
    ventana.title("Reproductor MP3")
    ventana.geometry("400x300")
    ventana.resizable(False, False)

    if (archivoCargado):
        label = tk.Label(ventana, text=f"Archivo cargado:\n{rutaCancion.split("/")[-1]}", wraplength=380)
    else:
        label = tk.Label(ventana, text="No se pudo carga el archivo MP3", fg="red")
    
    label.pack(pady=10)
    label_state = tk.Label(ventana, text="Reproductor inactivo", fg="gray")
    label_state.pack(pady=5)

    # Se crean los botones del reproductor
    frame_btns = tk.Frame(ventana)
    frame_btns.pack(pady=15)

    btn_play = tk.Button(frame_btns, text="Reproducir", command=reproducirCancion, state="normal" if archivoCargado else "disabled")
    btn_play.grid(row=0, column=0, padx=5)
    btn_pausar = tk.Button(frame_btns, text="Pausar", command=pausarCancion, state="normal" if archivoCargado else "disabled")
    btn_pausar.grid(row=0, column=1, padx=5)
    btn_continuar = tk.Button(frame_btns, text="Continuar", command=continuarCancion, state="normal" if archivoCargado else "disabled")
    btn_continuar.grid(row=0, column=2, padx=5)
    btn_detener = tk.Button(frame_btns, text="Detener", command=detenerCancion, state="normal" if archivoCargado else "disabled")
    btn_detener.grid(row=0, column=3, padx=5)

    # Control del volumen
    label_volume = tk.Label(ventana, text="Volumen al 70%")
    label_volume.pack(pady=5)

    volumenControl = ttk.Scale(
        ventana,
        from_=0,
        to=1,
        orient="horizontal",
        value=0.7,
        command=ajustarVolumen,
        length=250
    )

    volumenControl.pack()

    pygame.mixer.music.set_volume(0.7)

    # Ejecutamos la ventana del reproductor
    ventana.mainloop()