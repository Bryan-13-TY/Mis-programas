import os, json, socket, msvcrt
from Producto import listarArticulos, busqueda, limpiarTerminal

def getch():
    return msvcrt.getch().decode("utf-8")  # devuelve la tecla como string

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creamos al cliente
cliente.connect(("127.0.0.1", 5000)) # Nos conectamos con el servidor

while (True):
    limpiarTerminal()
    print("""
/*---------------------------.
| TIENDA EN LÍNEA: LALITOXDE |
`---------------------------*/

>> Elije una de las opciones
      
1.- Listar artículos de la tienda
2.- Buscar un artículo
3.- Agregar artículos al carrito de compra
4.- Editar el contenido del carrito
5.- Finalizar la compra
6.- Salir de la tienda
""")

    opcion = input("Opción: ")

    match (opcion):
        case '1':
            print("""
/*-------------------.
| LISTA DE ARTÍCULOS |                  
`-------------------*/
""")
            solicitud = {"accion": "LISTAR_ARTICULOS"}
            cliente.send(json.dumps(solicitud).encode("utf-8")) # Enviamos la solicitud serializada
            data = cliente.recv(4096).decode() # Deserializa los datos recibidos
            articulos = json.loads(data)
            listarArticulos(articulos) # Se listan los artículos
            print("\n>> Presiona una tecla para continuar...")
            tecla = getch()
        case '2':
            print("""
/*-------------------.
| BUSCAR UN ARTÍCULO |                  
`-------------------*/
""")
        case '3':
            print("""
/*------------------------------------------.
| AGREGAR UN ARTÍCULO AL CARRITO DE COMPRAS |
`------------------------------------------*/
""")
        case '4':
            print("""
/*----------------------------.
| EDITAR EL CARRITO DE COMPRA |                  
`----------------------------*/
""")
        case '5':
            print("""
/*--------------------.
| FINALIZAR LA COMPRA |                  
`--------------------*/
""")
        case '6':
            print("\n>> Gracias por visitar nuestra tienda, esperamos volverte a ver")
            cliente.close()
            break
        case _:
            print(">> La opción no es válida")