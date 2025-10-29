import tkinter as tk

class Sala:
    def __init__(self, nombreSala: str) -> None:
        self.nombre_sala = nombreSala

    def crearSala(self, window_size: str):
        sala = tk.Tk()
        sala.title(f"Sala: '{self.nombre_sala}'")
        sala.geometry(window_size)
        sala.resizable(False, False)

        return sala
    
    def crearLabel(self, sala, background_frame: str, border_frame: int, x: int, y: int):
        labels = tk.Frame(sala, background=background_frame, border=border_frame)
        labels.pack(padx=x, pady=y)

        return labels

    def agregarLabel(self, frame, text_label: str, font_label: tuple[str, int], text_color: str, width_text: int, background_color_text: str, x: int, y: int):
        label = tk.Label(frame, text=text_label, font=font_label, fg=text_color, wraplength=width_text, background=background_color_text)
        label.pack(padx=x, pady=y)