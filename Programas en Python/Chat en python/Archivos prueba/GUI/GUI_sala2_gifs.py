import tkinter as tk
from tkinter import ttk
import json
from pathlib import Path
from PIL import Image, ImageTk, ImageSequence

fuente = "Cascadia Code"
white = "#ffffff"
gray_1 = "#222429"
gray_2 = "#31343B"
gray_3 = "#363940"
discord = "#5567E3"

def cargar_usuarios() -> list[str]:
    """
    Obtiene la lista de los usuarios conectados en la sala.
    """
    carpeta_script = Path(__file__).parent
    ruta_usarios = carpeta_script/"usuarios.json"

    try:
        with open(ruta_usarios, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return ["Sin usuarios conectados"]
    
def enviar_mensaje() -> None:
    """
    Obtiene el mensajes del Entry y lo muestra en el widget Text.
    """
    texto = entrada_mensaje.get()

    if (texto.strip()):
        area_mensajes.insert(tk.END, f"Usuario: {texto}\n")
        entrada_mensaje.delete(0, tk.END)

def construir_interfaz(sala, nombre_sala: str):
    global area_mensajes, entrada_mensaje

    # Se configura el tamaño de la columnas
    sala.columnconfigure(0, weight=4) # Para el chat
    sala.columnconfigure(1, weight=1) # Para la lista de usuarios
    sala.rowconfigure(1, weight=1)

    # /-----------------------------.
    # | FRAME DEL TÍTULO DE LA SALA |
    # `-----------------------------/
    frame_titulo_sala = tk.Frame(sala, bg=gray_1, pady=4)
    frame_titulo_sala.grid(row=0, column=0, columnspan=5, sticky="we")
    titulo_sala = tk.Label(frame_titulo_sala, text=nombre_sala, font=(fuente, 16, "bold"), fg=white, bg=gray_1)
    titulo_sala.pack()

    # /-----------------------------------.
    # | FRAME PRINCIPAL (Chat y Usuarios) |
    # `-----------------------------------/
    frame_principal = tk.Frame(sala, bg=gray_2)
    frame_principal.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)

    # Se configura el tamaño de la columnas
    frame_principal.columnconfigure(0, weight=4)
    frame_principal.columnconfigure(1, weight=1)
    frame_principal.rowconfigure(0, weight=1)

    # /-----------------------.
    # | FRAME DE LOS MENSAJES |
    # `-----------------------/
    frame_chat = tk.Frame(frame_principal, bg=gray_3, bd=2)
    frame_chat.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
    titulo_chat = tk.Label(frame_chat, text="Mensajes del chat", font=(fuente, 12, "bold"), fg=white, bg=gray_3)
    titulo_chat.pack(pady=5)

    # Mensajes con scroll
    area_scroll = tk.Scrollbar(frame_chat)
    area_scroll.pack(side=tk.RIGHT, fill=tk.Y) # Scrollbar a la derecha del chat

    area_mensajes = tk.Text(frame_chat, bg=gray_2, fg=white, font=(fuente, 11), yscrollcommand=area_scroll.set, wrap="word", height=15)
    area_mensajes.pack(fill="both", expand=True, padx=10, pady=5)

    area_scroll.config(command=area_mensajes.yview)

    # /-------------------------------.
    # | FRAME DE LA LISTA DE USUARIOS |
    # `-------------------------------/
    frame_usuarios = tk.Frame(frame_principal, bg=gray_3)
    frame_usuarios.grid(row=0, column=1, sticky="nsew")
    titulo_usuarios = tk.Label(frame_usuarios, text="Usuarios conectados", font=(fuente, 12, "bold"), fg=white, bg=gray_3)
    titulo_usuarios.pack(pady=5)

    usuarios = cargar_usuarios()
    lista = tk.Listbox(frame_usuarios, bg=gray_2, fg=white, font=(fuente, 11), selectbackground=discord, relief="flat")
    lista.pack(fill="both", expand=True, padx=10, pady=5)

    for usuario in usuarios:
        lista.insert(tk.END, usuario)

    # /------------------------------------.
    # | FRAME DE LA ZONA DE ENVIAR MENSAJE |
    # `------------------------------------/
    frame_input = tk.Frame(sala, bg=gray_2, pady=10)
    frame_input.grid(row=2, column=0, columnspan=5, sticky="we", padx=10)

    entrada_mensaje = tk.Entry(frame_input, font=(fuente, 12), bg=gray_3, fg=white, relief="flat")
    entrada_mensaje.grid(row=0, column=0, sticky="we", padx=(10, 10))
    
    frame_input.columnconfigure(0, weight=1)

    btn_enviar = tk.Button(frame_input, text="Enviar", font=(fuente, 12, "bold"), bg=discord, fg=white, relief="flat", command=enviar_mensaje)
    btn_enviar.grid(row=0, column=1, padx=(0, 10))
    
    
    # /-------------------------------------.
    # | FRAME DE LA ZONA DE GIFS (STICKERS) |
    # `-------------------------------------/
    
    frame_gifs = tk.Frame(frame_principal, bg=gray_2, pady=10)
    frame_gifs.grid(row=2, column=0, columnspan=5, sticky="we", padx=10)
    
    titulo_stickers = tk.Label(frame_gifs, text="Stickers", font=(fuente, 12, "bold"), fg=white, bg=gray_3)
    titulo_stickers.pack(side="left", anchor="w", pady=5)
    
    # GIF 1
    gif1 = Image.open("emoji_crying.gif")

    frames1 = []
    for frame1 in ImageSequence.Iterator(gif1):
        frame1 = frame1.copy().resize((70, 70), Image.LANCZOS) # Cambiar tamaño de cada GIF (70x70)
        frames1.append(ImageTk.PhotoImage(frame1))

    label1 = tk.Label(frame_gifs)
    label1.pack(side="left", padx=10)

    def animar1(i=0):
        label1.config(image=frames1[i])
        sala.after(50, animar1, (i+1) % len(frames1))  # Cambia cada 50 ms

    animar1()
    
    # GIF 2
    gif2 = Image.open("emoji_laughing.gif")

    frames2 = []
    for frame2 in ImageSequence.Iterator(gif2):
        frame2 = frame2.copy().resize((70, 70), Image.LANCZOS) # Cambiar tamaño de cada GIF (70x70)
        frames2.append(ImageTk.PhotoImage(frame2))
        
    label2 = tk.Label(frame_gifs)
    label2.pack(side="left", padx=10)

    def animar2(i=0):
        label2.config(image=frames2[i])
        sala.after(50, animar2, (i+1) % len(frames2))  # Cambia cada 50 ms

    animar2()
    
    # GIF 3
    gif3 = Image.open("jijija.gif")

    frames3 = []
    for frame3 in ImageSequence.Iterator(gif3):
        frame3 = frame3.copy().resize((70, 70), Image.LANCZOS) # Cambiar tamaño de cada GIF (70x70)
        frames3.append(ImageTk.PhotoImage(frame3))
        
    label3 = tk.Label(frame_gifs)
    label3.pack(side="left", padx=10)

    def animar3(i=0):
        label3.config(image=frames3[i])
        sala.after(50, animar3, (i+1) % len(frames3))  # Cambia cada 50 ms

    animar3()

def crear_sala(root, nombre_sala: str):
    # Se crea la interfaz de la sala
    root.title(nombre_sala)
    root.geometry("900x600") # Ancho x alto
    root.resizable(False, False) # Ancho x alto
    root.configure(bg=gray_1)

    return nombre_sala

def main() -> None:
    sala1 = tk.Tk()
    nombre_sala1 = crear_sala(sala1, "Lalito XDE")
    construir_interfaz(sala1, nombre_sala1)

    sala1.mainloop()

if (__name__ == "__main__"):
    main()