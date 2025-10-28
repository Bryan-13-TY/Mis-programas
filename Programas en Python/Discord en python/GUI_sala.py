import tkinter as tk
from tkinter import ttk

def ventana(nombre_sala: str) -> None:
    ventana = tk.Tk()
    ventana.title(f"Sala {nombre_sala}")
    ventana.geometry("400x300")
    ventana.resizable(False, False)
    ventana.mainloop()

def main():
    nombre_sala = "LalitoXDE"
    ventana(nombre_sala)

if (__name__ == "__main__"):
    main()