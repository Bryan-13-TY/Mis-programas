import tkinter as tk
from tkinter import ttk
import json
from pathlib import Path

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

def main() -> None:
    global area_mensajes, entrada_mensaje

    # Se crea la interfaz de la sala
    sala = tk.Tk()
    sala.title("Sala: Sgt Pepper's Lonely Hearts Club Band")
    sala.geometry("900x600") # Ancho x alto
    sala.resizable(False, False) # Ancho x alto
    sala.configure(bg=gray_1)

    # Se configura el tamaño de la columnas
    sala.columnconfigure(0, weight=4) # Para el chat
    sala.columnconfigure(1, weight=1) # Para la lista de usuarios
    sala.rowconfigure(1, weight=1)

    # /-----------------------------.
    # | FRAME DEL TÍTULO DE LA SALA |
    # `-----------------------------/
    frame_titulo_sala = tk.Frame(sala, bg=gray_1, pady=4)
    frame_titulo_sala.grid(row=0, column=0, columnspan=5, sticky="we")
    titulo_sala = tk.Label(frame_titulo_sala, text="Sala: Sgt Pepper's Lonely Hearts Club Band", font=(fuente, 16, "bold"), fg=white, bg=gray_1)
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

    sala.mainloop() # Mostramos la sala

if (__name__ == "__main__"):
    main()