import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

prueba_gif = tk.Tk()

gif = Image.open("SkyPath_Gif_1_1152x648.gif")

frames = []
for frame in ImageSequence.Iterator(gif):
    frame = frame.copy().resize((200, 200), Image.LANCZOS) # Cambiar tamaño de cada frame
    frames.append(ImageTk.PhotoImage(frame))

label = tk.Label(prueba_gif)
label.pack()

def animar(i=0):
    label.config(image=frames[i])
    prueba_gif.after(20, animar, (i+1) % len(frames))  # Cambia cada 20 ms

animar()

prueba_gif.mainloop()
