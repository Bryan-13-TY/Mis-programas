def diccionarios():
    usuarios = [{"nombre": "Bryan", "edad": 21}, {"nombre": "Ximena"}, {"nombre": "Frida", "edad": 20}]
    
    for i, usuario in enumerate(usuarios):
        print(f"Usuario {i}.- Nombre: {usuario["nombre"]}, Edad: {usuario.get("edad", "desconocida")}")

def unir_cadenas():
    nombres = ["Ana", "Luis", "Samuel", "Ambar"]

    print(", ".join(nombres))

def invertir():
    lista = [i for i in range(50)]
    cadena = "Vive una vida que recuerdes"

    print(f"Lista invertida: {lista[::-1]}")
    print(f"Cadena invertida: {cadena[::-1]}")

def main():
    invertir()

if (__name__ == "__main__"):
    main()