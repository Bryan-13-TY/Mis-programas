import os, json

def obtenerRuta():
    carpetaScript = os.path.dirname(os.path.abspath(__file__))
    rutaJSON = os.path.join(carpetaScript, "articulos.json")

    return rutaJSON

def leerJSON(rutaArticulos: str):
    with open(rutaArticulos, "r", encoding = "utf-8") as file:
        data = json.load(file)

    return data

def actualizarJSON(rutaArticulos: str, data):
    with open(rutaArticulos, "w", encoding = "utf-8") as file:
        json.dump(data, file, indent = 4, ensure_ascii = False)

# Función para leer todos los artículos y guardarlos en un diccionario
def guardarArticulos(rutaArticulos: str):
    with open(rutaArticulos, "r", encoding = "utf-8") as file:
        articulos = json.load(file) # Guardamos los artículo en un diccionario

    return articulos

def listarTipo(articulos: dict, tipoArticulo: str):
    for art in articulos["articulos"]:
        if (art['tipo'] == tipoArticulo): # Si coincide con el tipo del artículo
            print(f"\nId: {art['id']}")
            print(f"Nombre: {art['nombre']}")
            print(f"Precio: ${art['precio']} MXN")
            print(f"Marca: {art['marca']}")
            print(f"Stock: {art['stock']} artículos disponibles")

def listarArticulos(articulos: dict):
    print("Lista de artículos de la tienda:\n")

    print("__Artículos de tipo Abarrotes__")
    listarTipo(articulos, "Abarrotes")
    print("\n__Artículos de tipo Bebidas__")
    listarTipo(articulos, "Bebidas")
    print("\n__Artículos de tipo Snacks__")
    listarTipo(articulos, "Snacks")
    print("\n__Artículos de tipo Cuidado personal__")
    listarTipo(articulos, "Cuidado personal")
    print("\n__Artículos de tipo Limpieza__")
    listarTipo(articulos, "Limpieza")

def busqueda(busqueda: dict):
    print("Artículo(s) encontrado(s):")
    for art in busqueda["articulos"]:
        print(f"\nId: {art['id']}")
        print(f"Tipo: {art['tipo']}")
        print(f"Nombre: {art['nombre']}")
        print(f"Precio: ${art['precio']} MXN")
        print(f"Marca: {art['marca']}")
        print(f"Stock: {art['stock']}")

def limpiarTerminal():
    os.system('cls' if os .name == 'nt' else 'clear')