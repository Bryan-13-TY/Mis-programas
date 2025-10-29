import tkinter as tk
from tkinter import ttk
from sala import Sala

def main():
    print("""
/*------------------.
| CREACIÓN DE SALAS |              
`------------------*/
""")
    
    sala1 = Sala("Lalito XDE")
    salaCreada1 = sala1.crearSala("700x500")
    label1_frame_sala1 = sala1.crearLabel(salaCreada1, "red", 10, 0, 0)
    sala1.agregarLabel(label1_frame_sala1, "Hello I'm John Lennon", ("Cascadia Code", 14), "red", 380, "black", 0, 0)
    sala1.agregarLabel(label1_frame_sala1, "Soy el fundador de The Beatles", ("Cascadia Code", 20), "green", 380, "blue", 0, 0)

    sala2 = Sala("AfterR")
    salaCreada2 = sala2.crearSala("300x400")
    label1_frame_sala2 = sala2.crearLabel(salaCreada2, "red", 10, 0, 0)
    sala2.agregarLabel(label1_frame_sala2, "Hello I'm Paul McCartney", ("Cascadia Code", 14), "red", 380, "yellow", 0, 0)

    salaCreada1.mainloop()
    salaCreada2.mainloop()

if (__name__ == "__main__"):
    main()