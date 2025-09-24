import os, json, socket
from Producto import listarArticulos, busqueda

def limpiarTerminal():
    os.system('cls' if os .name == 'nt' else 'clear')

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creamos al cliente
cliente.connect(("127.0.0.1", 5000)) # Nos conectamos con el servidor

while (True):
    #limpiarTerminal()
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
            cliente.send(b"LISTAR_ARTICULOS") # Enviamos solicitud al servidor

            # Recibir respuesta del servidor
            data = cliente.recv(4096).decode() # Deserializa los satos recibidos
            articulos = json.loads(data)

            listarArticulos(articulos) # Se listan los artículos
        case '2':
            print("""
/*-------------------.
| BUSCAR UN ARTÍCULO |                  
`-------------------*/
""")
            buscar = input("Escribe el nombre o la marca del artículo a buscar: ")

            # Armamos la solicitud en JSON
            cliente.send(json.dumps({"accion": "BUSCAR_ARTICULOS", "valor": buscar}).encode("utf-8")) # Enviamos la solicitud serializada a servidor

            # Creamos la respuesta desde el servidor
            data = b""
            
            while True:
                chunk = cliente.recv(4096)

                if (not chunk): # Si no hay nada recibido
                    break
                
                data += chunk # Concatenamos la respuesta

            respuesta = json.loads(data.decode("utf-8"))

            if "error" in respuesta:
                print(">> ", respuesta["error"])
            else:
                busqueda(respuesta)
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
            print(">> Gracias por visitar nuestra tienda, esperemos volverte a ver")
        case _:
            print(">> La opción no es válida")