import tkinter as tk
from tkinter import ttk

fuente = "Cascadia Code"
white = "#ffffff"
gray_1 = "#222429"
gray_2 = "#31343B"
gray_3 = "#363940"
discord = "#5567E3"

def main():
    # Se crea la interfaz de la sala
    sala = tk.Tk()
    sala.title("Sala Lalito XDE")
    sala.geometry("800x500") # Ancho y alto
    sala.resizable(False, False) # Ancho y alto

    # Cremos el título de la sala
    frame_titulo_sala = tk.Frame(sala, bg=gray_1, pady=4)
    frame_titulo_sala.grid(row=0, column=0, columnspan=5) # Se expande horizontalmente

    titulo_sala = tk.Label(frame_titulo_sala, text="Sala: Sgt Pepper's Lonely Hearts Club Band", font=(fuente, 16, "bold"), fg=white, bg=gray_1)
    titulo_sala.pack()

    # Creamos el frame donde se muestran los mensajes de la sala y los usuarios conectados
    frame_chat = tk.Frame(sala, bg=gray_2)
    frame_chat.grid(row=1, column=0, columnspan=5)

    # Creamos el frame donde se muestran los mensajes
    frame_titulo_mensaje = tk.Frame(frame_chat, bg=gray_2)
    frame_titulo_mensaje.grid(row=1, column=0, columnspan=3)
    titulo_mensaje = tk.Label(frame_titulo_mensaje, text="Mensajes del chat", font=(fuente, 12), fg=white, bg=gray_3)
    titulo_mensaje.pack()


    # Creamos el frama donde se muestran los usuarios conectados
    frame_titulo_usuarios = tk.Frame(frame_chat, bg=gray_2)
    frame_titulo_usuarios.grid(row=1, column=1, columnspan=2)
    titulo_usuarios = tk.Label(frame_titulo_usuarios, text="Usuarios conectados", font=(fuente, 12), fg=white, bg=gray_3)
    titulo_usuarios.pack()

    sala.mainloop() # Mostramos la sala

if (__name__ == "__main__"):
    main()