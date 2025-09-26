import os, json, socket, msvcrt
from Producto import listarArticulos, limpiarTerminal, mostrarBusqueda, mostrarMensaje

def getch():
    return msvcrt.getch().decode("utf-8")  # devuelve la tecla como string

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creamos al cliente
cliente.connect(("127.0.0.1", 5000)) # Nos conectamos con el servidor

while (True): # Mientras no se cierre el cliente
    limpiarTerminal()
    print("""
/*---------------------------.
| TIENDA EN LÍNEA: LALITOXDE |
`---------------------------*/

>> Elije una de las opciones
      
1.- Listar artículos de la tienda
2.- Buscar un artículo
3.- Carrito de compras
4.- Finalizar la compra
5.- Salir de la tienda
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
            articulos = json.loads(data) # Se convierte de JSON a diccionario
            listarArticulos(articulos) # Se listan los artículos
            print("\n>> Presiona una tecla para continuar...")
            tecla = getch()
        case '2':
            print("""
/*-------------------.
| BUSCAR UN ARTÍCULO |                  
`-------------------*/
""")
            buscar = input("Escribe el nombre o la marca del artículo(s) a buscar: ")
            solicitud = {"accion": "BUSCAR_ARTICULOS", "buscar": buscar}
            cliente.send(json.dumps(solicitud).encode("utf-8")) # Enviamos la solicitud serializada
            data = cliente.recv(4096).decode() # Deserializa los datos recibidos
            busqueda = json.loads(data) # Se convierte de JSON a diccionario

            if ("mensaje" in busqueda): # Si no hubo coincidencias
                mostrarMensaje(busqueda)
            else: # Si hubo al menos una coincidencia
                mostrarBusqueda(busqueda) # Se muestran los artículos encontrados
            print("\n>> Presiona una tecla para continuar...")
            tecla = getch()
        case '3':
            while (True):
                limpiarTerminal()
                print("""
/*-------------------.
| CARRITO DE COMPRAS |
`-------------------*/
                  
>> Elije una de las opciones

1.- Ver carrito
2.- Agregar un artículo al carrito
3.- Eliminar un artículo del carrito
4.- Volver
""")
                opcion = input("Opción: ")

                match (opcion):
                    case '1':
                        print("""
/*------------------------.
| ARTÍCULOS EN EL CARRITO |                              
`------------------------*/
""")
                        solicitud = {"accion": "MOSTRAR_CARRITO"}
                        cliente.send(json.dumps(solicitud).encode("utf-8"))
                    case '2':
                        print("""
/*-----------------.
| AGREGAR ARTÍCULO |
`-----------------*/
""")
                        buscar = input("Escribe el id o el nombre del artículos a agregar: ")
                        cantidad = input("Escribe la cantidad a agregar de ese artículo: ")
                        solicitud = {"accion": "AGREGAR_CARRITO", "buscar": buscar, "cantidad": int(cantidad)}
                        cliente.send(json.dumps(solicitud).encode("utf-8"))
                        print("\n>> Presiona una tecla para continuar...")
                        tecla = getch()
                    case '3':
                        print("""
/*------------------.
| ELIMINAR ARTÍCULO |            
`------------------*/
""")
                        print("\n>> Presiona una tecla para continuar...")
                        tecla = getch()
                    case '4':
                        break
                    case _:
                        print("\n>> La opción no es válida")
                        print("\n>> Presiona una tecla para continuar...")
                        tecla = getch()
        case '4':
            print("""
/*--------------------.
| FINALIZAR LA COMPRA |                  
`--------------------*/
""")
        case '5':
            print("\n>> Gracias por visitar nuestra tienda, esperamos volverte a ver")
            cliente.close()
            break
        case _:
            print("\n>> La opción no es válida")
            print("\n>> Presiona una tecla para continuar...")
            tecla = getch()
