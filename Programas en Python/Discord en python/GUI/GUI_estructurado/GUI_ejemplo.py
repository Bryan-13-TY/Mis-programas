import tkinter as tk
from tkinter import ttk, messagebox

# Ventana principal
root = tk.Tk()
root.title("Formulario de Registro")
root.geometry("400x450")
root.resizable(False, False)

# =====================
#  FRAME SUPERIOR (TÍTULO)
# =====================
frame_titulo = tk.Frame(root, bg="#2E86C1", pady=10)
frame_titulo.pack(fill="x")

tk.Label(
    frame_titulo,
    text="Formulario de Registro",
    font=("Arial", 16, "bold"),
    fg="white",
    bg="#2E86C1"
).pack()

# =====================
#  FRAME PRINCIPAL (CAMPOS)
# =====================
frame_campos = tk.Frame(root, padx=20, pady=15)
frame_campos.pack(fill="both", expand=True)

# Nombre
tk.Label(frame_campos, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
entry_nombre = tk.Entry(frame_campos, width=30)
entry_nombre.grid(row=0, column=1)

# Edad
tk.Label(frame_campos, text="Edad:").grid(row=1, column=0, sticky="w", pady=5)
entry_edad = tk.Entry(frame_campos, width=10)
entry_edad.grid(row=1, column=1, sticky="w")

# Género (Radiobutton)
tk.Label(frame_campos, text="Género:").grid(row=2, column=0, sticky="w", pady=5)
genero = tk.StringVar(value="N/A")
tk.Radiobutton(frame_campos, text="Masculino", variable=genero, value="Masculino").grid(row=2, column=1, sticky="w")
tk.Radiobutton(frame_campos, text="Femenino", variable=genero, value="Femenino").grid(row=2, column=1, sticky="e")

# Lenguajes de programación (Checkbutton)
tk.Label(frame_campos, text="Lenguajes:").grid(row=3, column=0, sticky="nw", pady=5)
leng_python = tk.BooleanVar()
leng_c = tk.BooleanVar()
leng_java = tk.BooleanVar()

tk.Checkbutton(frame_campos, text="Python", variable=leng_python).grid(row=3, column=1, sticky="w")
tk.Checkbutton(frame_campos, text="C/C++", variable=leng_c).grid(row=4, column=1, sticky="w")
tk.Checkbutton(frame_campos, text="Java", variable=leng_java).grid(row=5, column=1, sticky="w")

# País (Listbox)
tk.Label(frame_campos, text="País:").grid(row=6, column=0, sticky="w", pady=5)
lista_paises = tk.Listbox(frame_campos, height=4, exportselection=False)
for pais in ["México", "Argentina", "España", "Colombia", "Chile"]:
    lista_paises.insert(tk.END, pais)
lista_paises.grid(row=6, column=1, sticky="w")

# =====================
#  FRAME INFERIOR (BOTONES Y RESULTADOS)
# =====================
frame_botones = tk.Frame(root, pady=10)
frame_botones.pack(fill="x")

# Función para procesar formulario
def enviar_formulario():
    nombre = entry_nombre.get()
    edad = entry_edad.get()
    pais = lista_paises.get(tk.ACTIVE)
    seleccionados = []
    if leng_python.get(): seleccionados.append("Python")
    if leng_c.get(): seleccionados.append("C/C++")
    if leng_java.get(): seleccionados.append("Java")
    
    # Validación simple
    if not nombre or not edad.isdigit():
        messagebox.showwarning("Advertencia", "Por favor, completa correctamente los campos de nombre y edad.")
        return
    
    resumen = (
        f"👤 Nombre: {nombre}\n"
        f"🎂 Edad: {edad}\n"
        f"⚧ Género: {genero.get()}\n"
        f"🌎 País: {pais}\n"
        f"💻 Lenguajes: {', '.join(seleccionados) if seleccionados else 'Ninguno'}"
    )
    
    messagebox.showinfo("Datos registrados", resumen)

# Botón principal
ttk.Button(frame_botones, text="Enviar", command=enviar_formulario).pack()

# Barra de progreso (solo decoración)
barra = ttk.Progressbar(frame_botones, length=300, mode="determinate")
barra.pack(pady=5)
barra['value'] = 100

# =====================
#  FOOTER
# =====================
tk.Label(root, text="Ejemplo de Tkinter GUI", font=("Arial", 9), fg="gray").pack(side="bottom", pady=5)

# Iniciar aplicación
root.mainloop()