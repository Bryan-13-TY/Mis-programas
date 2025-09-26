import json, socket
from FuncionesCliente import listarArticulos, limpiarTerminal, mostrarBusqueda
from FuncionesCliente import mostrarMensaje, mostrarCarrito, esperarTecla

# Cremos al cliente y lo conectamos al servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creamos al cliente (dirección IPv4, protocolo TCP)
cliente.connect(("127.0.0.1", 5000)) # Conectamos al cliente con el servidor (dirección IP, puerto)

# Menú del cliente
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
/*--------------------------------.
| LISTA DE ARTÍCULOS EN LA TIENDA |                  
`--------------------------------*/
""")
            solicitud = {"accion": "LISTAR_ARTICULOS"} # Creamos la solicitud como un diccionario
            cliente.send(json.dumps(solicitud).encode("utf-8")) # Enviamos al servidor la solicitud serializada
            datosRecibidos = cliente.recv(4096).decode() # Recibe y deserializa los datos recibidos desde el servidor

            articulos = json.loads(datosRecibidos) # Convierte los datos recibidos en JSON a un diccionario

            listarArticulos(articulos) # Lista los artículos de la tienda

            # Esperamos una tecla
            print("\n>> Presiona una tecla para continuar...")
            tecla = esperarTecla()

        case '2':
            print("""
/*-------------------.
| BUSCAR UN ARTÍCULO |                  
`-------------------*/
""")
            buscar = input("Escribe el nombre o la marca del/los artículo(s) a buscar: ")

            solicitud = {"accion": "BUSCAR_ARTICULOS", "buscar": buscar} # Creamos la solicitud como un diccionario
            cliente.send(json.dumps(solicitud).encode("utf-8")) # Enviamos al servidor la solicitud serializada
            datosRecibidos = cliente.recv(4096).decode() # Recibe y deserializa los datos recibidos desde el servidor

            resultadoBusqueda = json.loads(datosRecibidos) # Convierte los datos recibidos en JSON a un diccionario

            if ("mensaje" in resultadoBusqueda): # No hubo coincidencias
                mostrarMensaje(resultadoBusqueda)
            else: # Si hubo al menos una coincidencia
                mostrarBusqueda(resultadoBusqueda) # # Se muestran los artículos encontrados
            
            # Esperamos una tecla
            print("\n>> Presiona una tecla para continuar...")
            tecla = esperarTecla()

        case '3':
            # Menú para el carrito
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
                        solicitud = {"accion": "MOSTRAR_CARRITO"} # Creamos la solicitud como un diccionario
                        cliente.send(json.dumps(solicitud).encode("utf-8")) # Enviamos al servidor la solicitud serializada
                        datosRecibidos = cliente.recv(4096).decode() # Recibe y deserializa los datos recibidos desde el servidor

                        articulosCarrito = json.loads(datosRecibidos) # Convierte los datos recibidos en JSON a un diccionario

                        if ("mensaje" in articulosCarrito): # El carrito esta vacío
                            mostrarMensaje(articulosCarrito)
                        else: # Si hay al menos un artículo en el carrito
                            mostrarCarrito(articulosCarrito)

                        # Esperamos una tecla
                        print("\n>> Presiona una tecla para continuar...")
                        tecla = esperarTecla()

                    case '2':
                        print("""
/*-----------------.
| AGREGAR ARTÍCULO |
`-----------------*/
""")
                        agregar = input("Escribe el id o el nombre del artículo a agregar: ")
                        cantidad = input("Escribe la cantidad a agregar de ese artículo: ")

                        solicitud = {"accion": "AGREGAR_CARRITO", "articulo": buscar, "cantidad": int(cantidad)} # Creamos la solicitud como un diccionario
                        cliente.send(json.dumps(solicitud).encode("utf-8")) # Enviamos al servidor la solicitud serializada

                        # Esperamos una tecla
                        print("\n>> Presiona una tecla para continuar...")
                        tecla = esperarTecla()

                    case '3':
                        print("""
/*------------------.
| ELIMINAR ARTÍCULO |            
`------------------*/
""")
                        eliminar = input("Escribe el id o el nombre del artículo a eliminar: ")
                        cantidad = input("Escribe la cantidad a eliminar de ese artículo: ")

                        solicitud = {"accion": "ELIMINAR_CARRITO", "articulo": eliminar, "cantidad": int(cantidad)} # Creamos la solicitud como un diccionario
                        cliente.send(json.dumps(solicitud).encode("utf-8")) # Enviamos al servidor la solicitud serializada

                        # Esperamos una tecla
                        print("\n>> Presiona una tecla para continuar...")
                        tecla = esperarTecla()

                    case '4':
                        break

                    case _:
                        print("\n>> La opción no es válida")

                        # Esperamos una tecla
                        print("\n>> Presiona una tecla para continuar...")
                        tecla = esperarTecla()

        case '4':
            print("""
/*--------------------.
| FINALIZAR LA COMPRA |                  
`--------------------*/
""")
            solicitud = {"accion": "FINALIZAR_COMPRA"} # Creamos la solicitud como un diccionario

            # Esperamos una tecla
            print("\n>> Presiona una tecla para continuar...")
            tecla = esperarTecla()

        case '5':
            print("\n>> Gracias por visitar nuestra tienda, esperamos volverte a ver")
            cliente.close()
            break

        case _:
            print("\n>> La opción no es válida")

            # Esperamos una tecla
            print("\n>> Presiona una tecla para continuar...")
            tecla = esperarTecla()