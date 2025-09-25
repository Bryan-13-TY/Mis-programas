import os, json

def obtenerRuta() -> str:
    carpetaScript = os.path.dirname(os.path.abspath(__file__))
    rutaJSON = os.path.join(carpetaScript, "articulos.json")

    return rutaJSON

def leerJSON(rutaArticulos: str):
    with open(rutaArticulos, "r", encoding = "utf-8") as file:
        data = json.load(file)

    return data

def actualizarJSON(rutaArticulos: str, data) -> None:
    with open(rutaArticulos, "w", encoding = "utf-8") as file:
        json.dump(data, file, indent = 4, ensure_ascii = False)

# Función para leer todos los artículos y guardarlos en un diccionario
def guardarArticulos(rutaArticulos: str):
    with open(rutaArticulos, "r", encoding = "utf-8") as file:
        articulos = json.load(file) # Guardamos los artículo en un diccionario

    return articulos

def listarTipo(articulos: dict, tipoArticulo: str) -> None:
    for art in articulos["articulos"]:
        if (art['tipo'] == tipoArticulo): # Si coincide con el tipo del artículo
            print(f"\nId: {art['id']}")
            print(f"Nombre: {art['nombre']}")
            print(f"Precio: ${art['precio']} MXN")
            print(f"Marca: {art['marca']}")
            print(f"Stock: {art['stock']} artículos disponibles")

def listarArticulos(articulos: dict) -> None:
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

def mostrarBusqueda(busqueda: dict) -> None:
    print("\nArtículo(s) encontrado(s):")
    for art in busqueda["articulos"]:
        print(f"\nId: {art['id']}")
        print(f"Tipo: {art['tipo']}")
        print(f"Nombre: {art['nombre']}")
        print(f"Precio: ${art['precio']} MXN")
        print(f"Marca: {art['marca']}")
        print(f"Stock: {art['stock']}")

def mostrarMensaje(mensaje: dict) -> None:
    print("\nArículos(s) encontrados(s):")
    for msj in mensaje["mensaje"]:
        print(f"\n>> {msj['error']}")

def limpiarTerminal() -> None:
    os.system('cls' if os .name == 'nt' else 'clear')