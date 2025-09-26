import os
import json

def leerProducto(ruta: str) -> tuple[dict]:
    productosList = [] # Diccionario de productos
    productosLeidos = []

    with open(ruta, "r") as productos:
        contenido = productos.read()
        lineas = contenido.split("\n") # Se guarda cada línea sin el \n (devuelve una list)

    for linea in lineas:
        productosLeidos.append(linea.split("/"))

    for producto in productosLeidos:
        product = {
            'tipo': producto[0],
            'nombre': producto[1],
            'precio': producto[2],
            'marca': producto[3],
            'stock': producto[4] 
        }
        
        productosList.append(product)
    
    return productosList

carpetaScript = os.path.dirname(os.path.abspath(__file__))
rutaTXT = os.path.join(carpetaScript, "Productos.txt")

Productos = leerProducto(rutaTXT)
for i in Productos:
    print(f"Producto: {i}")