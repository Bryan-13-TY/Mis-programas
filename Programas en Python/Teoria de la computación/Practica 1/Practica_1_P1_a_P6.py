# Práctica 1: Alfabetos, lenguajes y expresiones regulares
# Integrantes: García Escamilla Bryan Alexis y Melendez Macedonio Rodrigo

import string # Módulo necesario para el rango del alfabeto
import random # Módulo necesario para generar los lenguajes aleatorios
from itertools import product # Módulo y función necesaria para la potencia del alfabeto
from itertools import combinations #Módulo y función necesaria para las subsecuencias de Cadena_W2

# Función que calcula la diferencia de Lenguaje_1 y Lenguaje_2  
def Resta_Lenguajes(Lenguaje_1,Lenguaje_2):
    Lenguaje_D = []

    if (type(Lenguaje_1) == str) or (type(Lenguaje_2) == str):
        Lenguaje_D = "-----No se pudo calcular la resta de lenguaje 1 menos lenguaje 2-----"

        return Lenguaje_D
    else:
        for Elemento in range(0,len(Lenguaje_1)):
            if (Lenguaje_1[Elemento] in Lenguaje_2) == True:
                continue
            else:
                Lenguaje_D.append(Lenguaje_1[Elemento])
    
    return Lenguaje_D

# Función para generar los lenguajes a partir del diccionario
def Lenguajes(Diccionario):
    Long_Diccionario = len(Diccionario)
    print("")
    Numero_Elementos = int(input("Ingrese la cantidad de elementos que tendrán los lenguajes a generar: "))

    if Numero_Elementos > len(Diccionario) or Numero_Elementos <= 0: # Si no se cumple con el # de elementos
        print("")
        print("-----Número de elementos fuera de rango, intente de nuevo")
        
        Lenguaje_1 = "-----El lenguaje 1 no se pudo generar-----" 
        Lenguaje_2 = "-----El lenguaje 2 no se pudo generar-----"

        return Lenguaje_1,Lenguaje_2
    else:
        Long_Elemento = int(input("Ingrese la longitud que va a tener cada elemento de los lenguajes: "))

        if Long_Elemento <= 0: #Si no se cumple la longitud de los elementos
            print("")
            print("-----Longitud de elementos fuera de rango, intente de nuevo")

            Lenguaje_1 = "-----El lenguaje 1 no se pudo generar-----" 
            Lenguaje_2 = "-----El lenguaje 2 no se pudo generar-----"

            return Lenguaje_1,Lenguaje_2
        else:
            Lenguaje_1 = []
            Lenguaje_2 = []
            S_Aux = ""

            for Iteracion in range(0,2): # Se repite dos veces, dado que son dos lenguajes
                # Genera número aleatorios sin que se repitan mediante un rango, en este caso la longitud del alfabeto
                Numeros_Aleatorios = random.sample(range(0,Long_Diccionario),Numero_Elementos) 

                # Genera los elementos aleatorios
                for Indice in range(0,Numero_Elementos): # Genera los elementos del lenguaje
                    for Indice2 in range(0,Long_Elemento): # Genera el elemento del lenguaje 
                        # Genera números aleatorios mediante un rango, pero se pueden repetir
                        Elemento_Aleatorio = random.randint(0,Long_Diccionario)

                        if Elemento_Aleatorio == Long_Diccionario: # Corrección del error en Elemento_Aleatorio
                            w = 0
                        else:
                            if Long_Elemento == 1 and Indice2 == 0: # Si cada elemento del lenguaje es de longitud 1
                                S_Aux = S_Aux + Diccionario[Numeros_Aleatorios[Indice]]
                            else: # Si cada elemento del lenguaje es mayor a 1
                                S_Aux = S_Aux + Diccionario[Elemento_Aleatorio]
                    
                    # Condiciones para los lenguajes
                    if Iteracion == 0:
                        # Agrega los elementos al Lenguaje_1
                        if len(S_Aux) == Long_Elemento: # Si el elemento generado cumple con la longitud dada
                            Lenguaje_1.append(S_Aux) # Agrega el elemento al Lenguaje_1
                        elif len(S_Aux) < Long_Elemento: #Si el elemento generado no cumple con la longitud dada (es menor)
                            if Long_Elemento == 1: # Si cada elemento del lenguaje es de longitud 1
                                S_Aux = S_Aux + Diccionario[Numeros_Aleatorios[Indice]] # Genera el elemento que falta (Corrección error en la interación)
                                Lenguaje_1.append(S_Aux) # Agrega el elemento al Lenguaje_1
                            else: # Si cada elemento del lenguaje es mayor a 1
                                i = 0
                                while i < (Long_Elemento - len(S_Aux)): # Genera y agrega los elementos que faltan para cumplir con la longitud
                                    if Elemento_Aleatorio == 0:
                                        S_Aux = S_Aux + Diccionario[Elemento_Aleatorio + 1]
                                    else:
                                        S_Aux = S_Aux + Diccionario[Elemento_Aleatorio - 1]
                                Lenguaje_1.append(S_Aux) # Agrega el elemento al Lenguaje_1
                        S_Aux = ""
                    else:
                        # Agrega los elementos al Lenguaje_2
                        if len(S_Aux) == Long_Elemento: # Si el elemento generado cumple con la longitud dada
                            Lenguaje_2.append(S_Aux) # Agrega el elemento al Lenguaje_2
                        elif len(S_Aux) < Long_Elemento: #Si el elemento generado no cumple con la longitud dada (es menor)
                            if Long_Elemento == 1: # Si cada elemento del lenguaje es de longitud 1
                                S_Aux = S_Aux + Diccionario[Numeros_Aleatorios[Indice]] # Genera el elemento que falta (Corrección error en la interación)
                                Lenguaje_2.append(S_Aux) # Agrega el elemento al Lenguaje_2
                            else: # Si cada elemento del lenguaje es mayor a 1
                                i = 0
                                while i < (Long_Elemento - len(S_Aux)): # Genera y agrega los elementos que faltan para cumplir con la longitud
                                    if Elemento_Aleatorio == 0:
                                        S_Aux = S_Aux + Diccionario[Elemento_Aleatorio + 1]
                                    else:
                                        S_Aux = S_Aux + Diccionario[Elemento_Aleatorio - 1]
                                Lenguaje_2.append(S_Aux) # Agrega el elemento al Lenguaje_2
                        S_Aux = ""
            
            return Lenguaje_1,Lenguaje_2

# Función para verificar si Cadena_W1 es un prefijo de Cadena_W2
def Prefijo(Cadena_W1,Cadena_W2):
    Prefijos_W2 = []
    Prefijo_W2 = ""
    Long_Cadena_W2 = len(Cadena_W2)
    i = 0

    # Se obtiene el prefijo correspondiente 
    while i < Long_Cadena_W2:
        for j in range(0,i + 1):
            Prefijo_W2 = Prefijo_W2 + Cadena_W2[j]
        i += 1
        
        Prefijos_W2.append(Prefijo_W2) # Agrega el Prefijo_W2 a Prefijos_W2
        Prefijo_W2 = "" # Se establece el valor inicial del Prefijo_W2
    Prefijos_W2.insert(0,"λ") # Se le agrega el elemento Lambda

    # Verificar si Cadena_W1 es prefijo de Cadena_W2 (devuelve resultado)
    return Cadena_W1 in Prefijos_W2,Prefijos_W2

# Función para verificar si Cadena_W1 es un sufijo de Cadena_W2
def Sufijo(Cadena_W1,Cadena_W2):
    Sufijos_W2 = []
    Sufijo_W2 = ""
    Long_Cadena_W2 = len(Cadena_W2)
    Cadena_W2_Inv = Cadena_W2[::-1]
    i = 0

    # Se obtiene el sufijo correspondiente
    while i < Long_Cadena_W2:
        for j in range(0,i + 1):
            Sufijo_W2 = Cadena_W2_Inv[j] + Sufijo_W2
        i += 1

        Sufijos_W2.append(Sufijo_W2) # Agrega el Sufijo_W2 a Sufijos_W2
        Sufijo_W2 = "" # Se establece el valor incial del Sufijo_W2
    Sufijos_W2.insert(0,"λ") # Se le agrega el elemento Lambda
    
    # Verificar si Cadena_W1 es sufijo de Cadena_W2 (devuelve resultado)
    return Cadena_W1 in Sufijos_W2,Sufijos_W2

# Función para verificar si Cadena_W1 es un prefijo propio de Cadena_W2
def Prefijo_Propio(Cadena_W1,Cadena_W2,Prefijos_W2):
    Prefijos_Propios_W2 = []
    Prefijos_Propios_W2.extend(Prefijos_W2)
    
    Prefijos_Propios_W2.remove("λ")
    Prefijos_Propios_W2.remove(Cadena_W2)

    # Verificar si Cadena_W1 es prefijo propio de Cadena_W2 (devuelve resultado)
    return Cadena_W1 in Prefijos_Propios_W2

# Función para verificar si Cadena_W1 es un sufijo propio de Cadena_W2
def Sufijo_Propio(Cadena_W1,Cadena_W2,Sufijos_W2):
    Sufijos_Propios_W2 = []
    Sufijos_Propios_W2.extend(Sufijos_W2)
    
    Sufijos_Propios_W2.remove("λ")
    Sufijos_Propios_W2.remove(Cadena_W2)

    # Verificar si Cadena_W1 es sufijo propio de Cadena_W2 (devuelve resultado)
    return Cadena_W1 in Sufijos_Propios_W2

# Función para verificar si Cadena_W1 es una subcadena de Cadena_W2
def Subcadena(Cadena_W1,Cadena_W2):
    Subcadenas_W2 = []
    Subcadena_W2 = ""
    Long_Cadena_W2 = len(Cadena_W2)
    i = 0
    k = 0

    # Se calcula la subcadena correspondiente
    while k < Long_Cadena_W2:
        while i < Long_Cadena_W2:
            for j in range(k,i + 1):
                Subcadena_W2 = Subcadena_W2 + Cadena_W2[j]
            i += 1
            
            if Subcadena_W2 == "":
                w = 0
            else:
                Subcadenas_W2.append(Subcadena_W2) # Agrega la Subcadena_W2 a Subcadenas_W2
                Subcadena_W2 = "" # Se establece el valor de la Subcadena_W2
        k += 1
        i = 0

    Subcadenas_W2.insert(0,"λ") # Se le agrega el elemento Lambda
    Subcadenas_W2_SR = list(set(Subcadenas_W2))

    # Verificar si Cadena_W1 es una subcadena de Cadena_W2 (devuelve resultado)
    return Cadena_W1 in Subcadenas_W2_SR,Subcadenas_W2_SR

# Función para verificar si Cadena_W1 es una subcadena propia de Cadena_W2
def Subcadena_Propia(Cadena_W1,Cadena_W2,Subcadenas_W2):
    Subcadenas_Propias_W2 = list(Subcadenas_W2)
    Subcadenas_Propias_W2.remove(Cadena_W2)
    Subcadenas_Propias_W2.remove("λ")

    Subcadenas_Propias_W2_SR = list(set(Subcadenas_Propias_W2))

    # Verificae si Cadena_W1 es una subcadena propia de Cadena_W2 (devuelve resultado)
    return Cadena_W1 in Subcadenas_Propias_W2_SR

# Función para verificar si Cadena_W1 es una subsecuencia de Cadena_W2
def Subsecuencias(Cadena_W1,Cadena_W2):
    Subsecuencias = []
    Aux = ""

    #Método 1
    #for i in range(1,len(Cadena) + 1):
    #    for Combinacion in combinations(Cadena,i):
    #        print(Combinacion)
    #        Subsecuencias.append("".join(Combinacion))
    #return Subsecuencias

    #Método 2
    for i in range(1,len(Cadena_W2) + 1):
        for Subsecuencia in combinations(Cadena_W2,i):
            for j in Subsecuencia:
                Aux = Aux + j
            
            Subsecuencias.append(Aux)
            Aux = ""
    
    # Verificar si Cadena_W1 es una subcadena de Cadena_W2 (devuelve resultado)
    return Cadena_W1 in Subsecuencias

# Función que engloba y da el resultado en conjunto de las 7 funciones anteriores
def Funciones_Juntas(Cadena_W1,Cadena_W2,Bool1,Bool2):
    if Bool1 == True and Bool2 == True: # Se evaluna si ambas cadenas fueron ingresadas correctamente
        Res_P,Prefijos_W2 = Prefijo(Cadena_W1,Cadena_W2)
        Res_S,Sufijos_W2 = Sufijo(Cadena_W1,Cadena_W2)
        Res_PP = Prefijo_Propio(Cadena_W1,Cadena_W2,Prefijos_W2)
        Res_SP = Sufijo_Propio(Cadena_W1,Cadena_W2,Sufijos_W2)
        Res_S,Subcadenas_W2 = Subcadena(Cadena_W1,Cadena_W2)
        Res_SP = Subcadena_Propia(Cadena_W1,Cadena_W2,Subcadenas_W2)
        Res_SC = Subsecuencias(Cadena_W1,Cadena_W2)

        # Resultados de las funciones de arriba  
        Resultados = ""
        
        if Res_P == True:
            Resultados = Resultados + "La cadena W1 SI es prefijo"
        else:
            Resultados = Resultados + "La cadena W1 NO es prefijo"
        
        if Res_S == True:
            Resultados = Resultados + ", SI es sufijo"
        else:
            Resultados = Resultados + ", NO es sufijo"

        if Res_PP == True:
            Resultados = Resultados + ", SI es prefijo propio"
        else:
            Resultados = Resultados + ", NO es prefijo propio"
        
        if Res_SP == True:
            Resultados = Resultados + ", SI es sufijo propio"
        else:
            Resultados = Resultados + ", NO es sufijo propio"
        
        if Res_S == True:
            Resultados = Resultados + ", SI es subcadena"
        else:
            Resultados = Resultados + ", NO es subcadena"

        if Res_SP == True:
            Resultados = Resultados + ", SI es una subcadena propia"
        else:
            Resultados = Resultados + ", NO es una subcadena propia"

        if Res_SC == True:
            Resultados = Resultados + ", SI es una subsecuencia de la cadena W2"
        else:
            Resultados = Resultados + ", NO es una subsecuencia de la cadena W2"
        
        return Resultados
    else:
        return "-----No se pudo determinar si la cadena W1 es predijo, sufijo, prefijo propio, sufijo propio, subcadena, subcadena propia o subsecuencia de la cadena W2-----" 

# Función que muestra los mensajes de error
def Mensajes_Error():
    Diccionario_Res = "-----El alfabeto no se pudo definir-----"
    Cadena_W1 = "-----La cadena W1 no se pudo definir-----"
    Cadena_W2 = "-----La cadena W2 no se pudo definir-----"
    Resultados = "-----No se pudo determinar si la cadena W1 es predijo, sufijo, prefijo propio, sufijo propio, subcadena, subcadena propia o subsecuencia de la cadena W2-----"
    Lenguaje_1 = "-----No se pudo generar el lenguaje 1-----"
    Lenguaje_2 = "-----No se pudo generar el lenguaje 2-----"
    Lenguaje_D = "-----No se pudo calcular la resta del lenguaje 1 menos lenguaje 2-----"
    Potencia_Res = "-----No se pudo mostrar el alfabeto elevado a una potencia puesto que el alfabeto no esta definido previamente-----"

    return Diccionario_Res,Cadena_W1,Cadena_W2,Resultados,Lenguaje_1,Lenguaje_2,Lenguaje_D,Potencia_Res

# Función que hace el calculo de la potencia del alfabeto
def Calculo_Potencia(Potencia,Diccionario):
    Potencia_Res = []
    Aux = ""
    
    Combinaciones = product(Diccionario,repeat = Potencia)
    #Método 1
    #Potencia_Res = ["".join(Combinacion) for Combinacion in Combinaciones]

    #Método 2
    #for i in Combinaciones:
    #    Combinacion = "".join(i)
    #    Potencia_Res.append(Combinacion)

    #Método 3
    for Tupla in list(Combinaciones):
        for Elemento in Tupla:
            Aux = Aux + Elemento

        Potencia_Res.append(Aux)
        Aux = ""
    
    return Potencia_Res

# Función que eleva el alfabeto a la potencia dada
def Potencia_Diccionario(Diccionario):
    print("")
    Potencia = int(input("Ingrese un número dentro del rango -5 a 5 para la potencia del alfabeto: "))
    if Potencia == 0:
        Potencia_Res = Calculo_Potencia(Potencia,Diccionario)
        Potencia_Res.remove("")
        Potencia_Res.append("λ")
        
        return f"El alfabeto elevado a la potencia {Potencia} es: {Potencia_Res}"
    elif Potencia > 5 or Potencia < -5:
        return "-----Ingrese un número dentro del rango establecido para la potencia, intente de nuevo-----"
    elif Potencia < 0 and Potencia > -6:
        Potencia2 = Potencia * -1
        Potencia_Res = Calculo_Potencia(Potencia2,Diccionario = Diccionario[::-1])
        
        return f"El alfabeto elevado a la potencia {Potencia} es: {Potencia_Res}"
    else:
        Potencia_Res = Calculo_Potencia(Potencia,Diccionario)
        
        return f"El alfabeto elevado a la potencia {Potencia} es: {Potencia_Res}"

# Función que verifica que ambas cadenas pertenezcan al alfabeto definido
def Verficar_Pertenencia(Diccionario):
    CW1 = set()
    print("")
    Cadena_W1 = input("Ingrese la cadena W1: ")
    for j in Cadena_W1:
        CW1.add(j)
        
    if (CW1.issubset(set(Diccionario))) == True:
        print("")
        print(f"-----La cadena {Cadena_W1} si pertenece al alfabeto definido-----")
        CW2 = set()
        print("")
        Cadena_W2 = input("Ingrese la cadena W2: ")
        for k in Cadena_W2:
            CW2.add(k)

        if (CW2.issubset(set(Diccionario))) == True:
            print("")
            print(f"-----La cadena {Cadena_W2} si pertenece al alfabeto definido-----")
            
            return Cadena_W1,Cadena_W2,True,True
        else:
            print("")
            print(f"-----La cadena {Cadena_W2} no pertenece al alfabeto definido-----")
            Cadena_W2 = f"-----La cadena {Cadena_W2} no pertenece al alfabeto definido-----"
            
            return Cadena_W1,Cadena_W2,True,False
    else:
        print("")
        print(f"-----La cadena {Cadena_W1} no pertenece al alfabeto definido-----")
        Cadena_W1 = f"-----La cadena {Cadena_W1} no pertenece al alfabeto definido-----"
        Cadena_W2 = "-----La cadena W2 no se pudo definir-----"
        
        return Cadena_W1,Cadena_W2,False,False

# Primera opción de llenado del abecedario (individual)
def Opcion_1():
    Diccionario = []
    i = 0
    
    print("""
-----Elegiste la opción 1-----
    """)

    CantDic = int(input("Escribe la cantidad de elementos del alfabeto: "))
    print("")
    
    # Se crea el diccionario para la opción 1
    if CantDic >= 3:
        while i < CantDic:
            Caracter = input("Escribe un carácter: ")
            if len(Caracter) > 1:
                print("")
                print("-----No se permite que un elemento del alfabeto tenga más de un carácter, intente de nuevo-----")
                
                # Mensajes de error
                Diccionario_Res,Cadena_W1,Cadena_W2,Resultados,Lenguaje_1,Lenguaje_2,Lenguaje_D,Potencia_Res = Mensajes_Error()
                
                return Diccionario_Res,Cadena_W1,Cadena_W2,Resultados,Lenguaje_1,Lenguaje_2,Lenguaje_D,Potencia_Res
            elif (Caracter in Diccionario) == True:
                print("")
                print("-----No puede haber elementos repetidos en el alfabeto, intente de nuevo-----")
                
                # Mensajes de error
                Diccionario_Res,Cadena_W1,Cadena_W2,Resultados,Lenguaje_1,Lenguaje_2,Lenguaje_D,Potencia_Res = Mensajes_Error()
                
                return Diccionario_Res,Cadena_W1,Cadena_W2,Resultados,Lenguaje_1,Lenguaje_2,Lenguaje_D,Potencia_Res
            else:
                # Se crea el diccionario
                Diccionario.append(Caracter)
                i += 1
 
        # Parte de las cadenas
        Cadena_W1,Cadena_W2,Bool1,Bool2 = Verficar_Pertenencia(Diccionario)

        # Parte de las combinaciones
        Resultados = Funciones_Juntas(Cadena_W1,Cadena_W2,Bool1,Bool2)

        # Parte de los lenguajes
        Lenguaje_1,Lenguaje_2 = Lenguajes(Diccionario)

        #Parte de la resta de los lenguajes
        Lenguaje_D = Resta_Lenguajes(Lenguaje_1,Lenguaje_2)

        # Parte de la potencia
        Potencia_Res = Potencia_Diccionario(Diccionario)
        
        return Diccionario,Cadena_W1,Cadena_W2,Resultados,Lenguaje_1,Lenguaje_2,Lenguaje_D,Potencia_Res
    else:
        print("-----El alfabeto debe tener 3 o más elementos, intente de nuevo-----")
        
        # Mensajes de error
        Diccionario_Res,Cadena_W1,Cadena_W2,Resultados,Lenguaje_1,Lenguaje_2,Lenguaje_D,Potencia_Res = Mensajes_Error()
        
        return Diccionario_Res,Cadena_W1,Cadena_W2,Resultados,Lenguaje_1,Lenguaje_2,Lenguaje_D,Potencia_Res

# Segunda opción de llenado del abecedario (rango)
def Opcion_2():
    Diccionario = []
    Cadena_Aux = string.printable
    Lista_Aux = []

    print("""
-----Elegiste la opción 2-----

Rangos aceptados: 0-9, a-z, A-Z, 0-Z o una combinación de ellos
    """)
    Rango = input("Escribe el rango del alfabeto de la forma Caracter_Inicio-Caracter_Final (el rango no debe de abarcar menos de 3 carácteres): ")
    
    # Se crea el diccionario para la opción 2
    R1 = Cadena_Aux.find(Rango[0])
    R2 = Cadena_Aux.find(Rango[2])

    # Crea una lista con los carácteres del rango ingresado
    for i in range(R1,R2 + 1):
        Lista_Aux.append(i)

    print(f"""
-----El alfabeto que definiste tiene una longitud de {len(Lista_Aux)}-----""")

    if R2 > R1 and len(Lista_Aux) >= 3 and len(Lista_Aux) < 63:
        # Se crea el diccionario
        for i in range(R1,R2 + 1):
            Diccionario.append(Cadena_Aux[i])
        
        # Parte de las cadenas
        Cadena_W1,Cadena_W2,Bool1,Bool2 = Verficar_Pertenencia(Diccionario)

        # Parte de las combinaciones
        Resultados = Funciones_Juntas(Cadena_W1,Cadena_W2,Bool1,Bool2)

        # Parte de los lenguajes
        Lenguaje_1,Lenguaje_2 = Lenguajes(Diccionario)

        # Parte de la resta de los lenguajes
        Lenguaje_D = Resta_Lenguajes(Lenguaje_1,Lenguaje_2)

        # Parte de la potencia
        Potencia_Res = Potencia_Diccionario(Diccionario)

        return Diccionario,Cadena_W1,Cadena_W2,Resultados,Lenguaje_1,Lenguaje_2,Lenguaje_D,Potencia_Res
    else:
        print("")
        print("-----Rango no válido, intente de nuevo-----")
        
        # Mensajes de error
        Diccionario_Res,Cadena_W1,Cadena_W2,Resultados,Lenguaje_1,Lenguaje_2,Lenguaje_D,Potencia_Res = Mensajes_Error()
        
        return Diccionario_Res,Cadena_W1,Cadena_W2,Resultados,Lenguaje_1,Lenguaje_2,Lenguaje_D,Potencia_Res
    
# Opción por default
def Default():
    # Mensajes de error
    Diccionario_Res,Cadena_W1,Cadena_W2,Resultados,Lenguaje_1,Lenguaje_2,Lenguaje_D,Potencia_Res = Mensajes_Error()
    
    return Diccionario_Res,Cadena_W1,Cadena_W2,Resultados,Lenguaje_1,Lenguaje_2,Lenguaje_D,Potencia_Res

# Menú del programa
def Menu(Opcion):
    Menu = {
        1: Opcion_1,
        2: Opcion_2
    }

    return Menu.get(Opcion,Default)()

# Menú del programa impreso
while True:

    print("""-----Práctica 1-----

Elija una de las opciones para definir el alfabeto a usar:
      
1.- Definir el alfabeto carácter por carácter
2.- Definir el alfabeto mediante un rango de carácteres
""")

    # Condición de salida basada en alguna lógica
    Opcion = int(input("Elija una opción: "))

    if Opcion != 1 and Opcion != 2:
        print(f"""
-----La opción {Opcion} no es válida, intente de nuevo-----""")

# Código que se repite al menos una vez
    Diccionario_Res,Cadena_W1,Cadena_W2,Resultados,Lenguaje_1,Lenguaje_2,Lenguaje_D,Potencia_Res = Menu(Opcion)
    
    if type(Diccionario_Res) == str:
        print(f"""
{Diccionario_Res}
{Cadena_W1}
{Cadena_W2}
{Resultados}
{Lenguaje_1}
{Lenguaje_2}
{Lenguaje_D}
{Potencia_Res}
""")
    else:
        print(f"""
- El alfabeto que definiste es: Σ = {Diccionario_Res} con longitud {len(Diccionario_Res)}

- La cadena W1 es: {Cadena_W1}

- La cadena W2 es: {Cadena_W2}

- {Resultados}

- El lenguaje 1 es: {Lenguaje_1}

- El lenguaje 2 es: {Lenguaje_2}

- El resultado de la resta del lenguaje 1 menos el lenguaje 2 es: {Lenguaje_D}

- {Potencia_Res}
""")