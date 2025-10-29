import tkinter as tk
from tkinter import ttk

#def labels(ventana) -> None:
    # Se crean los labels
#    labels = tk.Frame(ventana, background="red", border=10)
#    labels.pack(padx=0, pady=0) 

#    label = tk.Label(labels, text="Hello I'm John Lennon", font=("Cascadia Code", 14), fg="red", wraplength=380, background="black")
#    label.pack(padx=0, pady=0) # Se le puede poner padding (x, y)
#    label1 = tk.Label(labels, text="Hello I'm Paul McCartney", font=("Cascadia Code", 14), fg="green", wraplength=380, background="black")
#    label1.pack(padx=0, pady=0)
#    label2 = tk.Label(labels, text="Hello I'm George Harrison", font=("Cascadia Code", 14), fg="blue", wraplength=380, background="black")
#    label2.pack(padx=0, pady=0)
#    label3 = tk.Label(labels, text="Hello I'm Ringo Starr", font=("Cascadia Code", 14), fg="purple", wraplength=380, background="black")
#    label3.pack(padx=0, pady=0)

#def botones(ventana) -> None:
#    btns = tk.Frame(ventana)

#def crearSala(nombre_sala: str) -> None:
#    ventana = tk.Tk()
#    ventana.title(f"Sala {nombre_sala}")
#    ventana.geometry("700x500") # Ancho y alto
#    ventana.resizable(False, False) # Ancho y alto (se puede redimensionar)

#    labels(ventana)
#    botones(ventana)

#    ventana.mainloop()

def main():
    # Se crea la interfaza de la sala
    sala = tk.Tk()
    sala.title("Sala Lalito XDE")
    sala.geometry("700x500") # Ancho y alto
    sala.resizable(False, False) # Ancho y alto

    # Creamos el frame con el título de la sala
    frame_titulo = tk.Frame(sala, bg="#31343B", pady=4)
    frame_titulo.pack(fill="both")

    tk.Label(frame_titulo, text="Sala LALITO XDE", font=("Cascadia Code", 16, "bold"), fg="white", bg="#31343B").pack()

    # Creamos el frame para donde se muestran los mensajes y los usuaron conectados
    frame_chat = tk.Frame(sala, bg="#363940", padx=5, pady=5)
    frame_chat.pack(fill="both", expand=True)

    # Creamos el frame donde se muestran los mensajes
    frame_mensajes = tk.Frame(frame_chat, bg="red", padx=2)
    frame_mensajes.pack(side="left", fill="both", expand=True)
    tk.Label(frame_mensajes, text="Chat de la sala", font=("Cascadia Code", 14), fg="#363940", bg="#5567E3").pack(fill="x")

    frame_mensajes_content = tk.Frame(frame_mensajes, bg="red")
    frame_mensajes_content.pack()
    tk.Label(frame_mensajes_content, text="Bryan: Hola ¿Cómo estan?", font=("Cascadia Code", 10), fg="#363940").grid(row=0, column=0)
    tk.Label(frame_mensajes_content, text="Edwyn: Muy bien ¿Y tu?", font=("Cascadia Code", 10), fg="#363940").grid(row=1, column=0)

    # Creamos el frame donde se muestran los usuaruos conectados
    frame_users = tk.Frame(frame_chat, bg="blue", padx=2)
    frame_users.pack(side="right", fill="both", expand=True)
    tk.Label(frame_users, text="Usuarios en la sala", font=("Cascadia Code", 14), fg="#363940", bg="#5567E3").pack(fill="x")




    sala.mainloop() # Mostramos la sala

if (__name__ == "__main__"):
    main()

# #363940 Color fondo
# #31343B Color borde
# #5567E3 Color discord