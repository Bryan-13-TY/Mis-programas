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
    sala.geometry("800x500")  # Ancho x Alto
    sala.resizable(False, False)

    sala.configure(bg=gray_1)

    # =========================
    # FRAME TÍTULO SUPERIOR
    # =========================
    frame_titulo_sala = tk.Frame(sala, bg=gray_1, pady=6)
    frame_titulo_sala.grid(row=0, column=0, columnspan=4, sticky="we")

    titulo_sala = tk.Label(
        frame_titulo_sala,
        text="Sala: Sgt Pepper's Lonely Hearts Club Band",
        font=(fuente, 16, "bold"),
        fg=white,
        bg=gray_1
    )
    titulo_sala.pack()

    # =========================
    # FRAME PRINCIPAL (Chat + Usuarios)
    # =========================
    frame_chat = tk.Frame(sala, bg=gray_2)
    frame_chat.grid(row=1, column=0, columnspan=4, sticky="nsew")

    # Configurar tamaño proporcional de columnas
    sala.columnconfigure(0, weight=3)  # Chat más ancho
    sala.columnconfigure(1, weight=1)  # Lista usuarios
    sala.rowconfigure(1, weight=1)

    # =========================
    # SECCIÓN DE MENSAJES
    # =========================
    frame_mensajes = tk.Frame(frame_chat, bg=gray_3, bd=2)
    frame_mensajes.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    tk.Label(
        frame_mensajes,
        text="Mensajes del chat",
        font=(fuente, 12, "bold"),
        fg=white,
        bg=gray_3
    ).pack(pady=5)

    # =========================
    # SECCIÓN DE USUARIOS
    # =========================
    frame_usuarios = tk.Frame(frame_chat, bg=gray_3, bd=2)
    frame_usuarios.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    tk.Label(
        frame_usuarios,
        text="Usuarios conectados",
        font=(fuente, 12, "bold"),
        fg=white,
        bg=gray_3
    ).pack(pady=5)

    # Ajustar crecimiento dentro de frame_chat
    frame_chat.columnconfigure(0, weight=3)
    frame_chat.columnconfigure(1, weight=1)
    frame_chat.rowconfigure(0, weight=1)

    sala.mainloop()

if __name__ == "__main__":
    main()
