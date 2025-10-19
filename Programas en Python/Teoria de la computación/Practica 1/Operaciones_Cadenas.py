from itertools import combinations #Módulo y función necesaria para las subsecuencias de Cadena_W2

#Función para verificar si Cadena_W1 es un prefijo de Cadena_W2
def Prefijo(Cadena_W1,Cadena_W2):
    Prefijos_W2 = []
    Prefijo_W2 = ""
    Long_Cadena_W2 = len(Cadena_W2)
    i = 0

    #Se obtiene el prefijo correspondiente 
    while i < Long_Cadena_W2:
        for j in range(0,i + 1):
            Prefijo_W2 = Prefijo_W2 + Cadena_W2[j]
        i += 1
        
        Prefijos_W2.append(Prefijo_W2) #Agrega el Prefijo_W2 a Prefijos_W2
        Prefijo_W2 = "" #Se establece el valor inicial del Prefijo_W2
    Prefijos_W2.insert(0,"λ") #Se le agrega el elemento Lambda

    #Verificar si Cadena_W1 es prefijo de Cadena_W2
    return Cadena_W1 in Prefijos_W2,Prefijos_W2

#Función para verificar si Cadena_W1 es un sufijo de Cadena_W2
def Sufijo(Cadena_W1,Cadena_W2):
    Sufijos_W2 = []
    Sufijo_W2 = ""
    Long_Cadena_W2 = len(Cadena_W2)
    Cadena_W2_Inv = Cadena_W2[::-1]
    i = 0

    #Se obtiene el sufijo correspondiente
    while i < Long_Cadena_W2:
        for j in range(0,i + 1):
            Sufijo_W2 = Cadena_W2_Inv[j] + Sufijo_W2
        i += 1

        Sufijos_W2.append(Sufijo_W2) #Agrega el Sufijo_W2 a Sufijos_W2
        Sufijo_W2 = "" #Se establece el valor incial del Sufijo_W2
    Sufijos_W2.insert(0,"λ") #Se le agrega el elemento Lambda
    
    #Verificar si Cadena_W1 es sufijo de Cadena_W2
    return Cadena_W1 in Sufijos_W2,Sufijos_W2

#Función para verificar si Cadena_W1 es un prefijo propio de Cadena_W2
def Prefijo_Propio(Cadena_W1,Cadena_W2,Prefijos_W2):
    Prefijos_Propios_W2 = []
    Prefijos_Propios_W2.extend(Prefijos_W2)
    
    Prefijos_Propios_W2.remove("λ")
    Prefijos_Propios_W2.remove(Cadena_W2)

    #Verificar si Cadena_W1 es prefijo propio de Cadena_W2
    return Cadena_W1 in Prefijos_Propios_W2,Prefijos_Propios_W2

#Función para verificar si Cadena_W1 es un sufijo propio de Cadena_W2
def Sufijo_Propio(Cadena_W1,Cadena_W2,Sufijos_W2):
    Sufijos_Propios_W2 = []
    Sufijos_Propios_W2.extend(Sufijos_W2)
    
    Sufijos_Propios_W2.remove("λ")
    Sufijos_Propios_W2.remove(Cadena_W2)

    #Verificar si Cadena_W1 es sufijo propio de Cadena_W2
    return Cadena_W1 in Sufijos_Propios_W2,Sufijos_Propios_W2

#Función para verificar si Cadena_W1 es una subcadena de Cadena_W2
def Subcadena(Cadena_W1,Cadena_W2):
    Subcadenas_W2 = []
    Subcadena_W2 = ""
    Long_Cadena_W2 = len(Cadena_W2)
    i = 0
    k = 0

    #Se obtiene la subcadena correspondiente
    while k < Long_Cadena_W2:
        while i < Long_Cadena_W2:
            for j in range(k,i + 1):
                Subcadena_W2 = Subcadena_W2 + Cadena_W2[j]
            i += 1
            
            if Subcadena_W2 == "":
                w = 0
            else:
                Subcadenas_W2.append(Subcadena_W2) #Agrega la Subcadena_W2 a Subcadenas_W2
                Subcadena_W2 = "" #Se establece el valor de la Subcadena_W2
        k += 1
        i = 0
    Subcadenas_W2.insert(0,"λ") #Se le agrega el elemento Lambda
    Subcadenas_W2_SR = list(set(Subcadenas_W2))
    
    #Verificar si Cadena_W1 es una subcadena de Cadena_W2
    return Cadena_W1 in Subcadenas_W2_SR,Subcadenas_W2_SR

#Función para verificar si Cadena_W1 es una subcadena propia de Cadena_W2
def Subacdena_Propia(Cadena_W1,Cadena_W2,Subcadenas_W2):
    Subcadenas_Propias_W2 = list(Subcadenas_W2)
    Subcadenas_Propias_W2.remove(Cadena_W2)
    Subcadenas_Propias_W2.remove("λ")
    
    Subcadenas_Propias_W2_SR = list(set(Subcadenas_Propias_W2))
    return Cadena_W1 in Subcadenas_Propias_W2,Subcadenas_Propias_W2_SR

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
    return Cadena_W1 in Subsecuencias,Subsecuencias

#Función que engloba y da el resultado en conjunto de las 6 funciona anteriores
def Funciones_Juntas(Cadena_W1,Cadena_W2):
    Res_P,Prefijos_W2 = Prefijo(Cadena_W1,Cadena_W2)
    Res_S,Sufijos_W2 = Sufijo(Cadena_W1,Cadena_W2)
    Res_PP,Prefijos_Propios_W2 = Prefijo_Propio(Cadena_W1,Cadena_W2,Prefijos_W2)
    Res_SP,Sufijos_Propios_W2 = Sufijo_Propio(Cadena_W1,Cadena_W2,Sufijos_W2)
    Res_S,Subcadenas_W2 = Subcadena(Cadena_W1,Cadena_W2)
    Res_SP,Subcadenas_Propias_W2 = Subacdena_Propia(Cadena_W1,Cadena_W2,Subcadenas_W2)
    Res_SC,Subsecuencias_W2 = Subsecuencias(Cadena_W1,Cadena_W2)
    
    #Resultados = ""
    
    #if Res_P == True:
    #    Resultados = Resultados + f"La cadena {Cadena_W1} SI es prefijo"
    #else:
    #    Resultados = Resultados + f"La cadena {Cadena_W1} NO es prefijo"
    
    #if Res_S == True:
    #    Resultados = Resultados + ", SI es sufijo"
    #else:
    #    Resultados = Resultados + ", NO es sufijo"

    #if Res_PP == True:
    #    Resultados = Resultados + ", SI es prefijo propio"
    #else:
    #    Resultados = Resultados + ", NO es prefijo propio"
    
    #if Res_SP == True:
    #    Resultados = Resultados + ", SI es sufijo propio"
    #else:
    #    Resultados = Resultados + ", NO es sufijo propio"
    
    #if Res_S == True:
    #    Resultados = Resultados + ", SI es subcadena"
    #else:
    #    Resultados = Resultados + ", NO es subcadena"

    #if Res_SP == True:
    #    Resultados = Resultados + f", SI es una subcadena propia"
    #else:
    #    Resultados = Resultados + f", NO es una subcadena propia"
    
    #if Res_SC == True:
    #    Resultados = Resultados + f", SI es una subsecuencia de la cadena {Cadena_W2}"
    #else:
    #    Resultados = Resultados + f", NO es una subecuencia de la cadena {Cadena_W2}"
    

    #return Resultados

    return Prefijos_W2,Sufijos_W2,Prefijos_Propios_W2,Sufijos_Propios_W2,Subcadenas_W2,Subcadenas_Propias_W2,Subsecuencias_W2
    
#Esto va dentro de las funciones Opcion_1() y Opcion_2()
Cadena_W1 = "0"
Cadena_W2 = "abc"

#Resultados = Funciones_Juntas(Cadena_W1,Cadena_W2)

Prefijos_W2,Sufijos_W2,Prefijos_Propios_W2,Sufijos_Propios_W2,Subcadenas_W2,Subcadenas_Propias_W2,Subsecuencias_W2 = Funciones_Juntas(Cadena_W1,Cadena_W2)

print(f"Prefijos: {Prefijos_W2}")
print("")
print(f"Sufijos: {Sufijos_W2}")
print("")
print(f"Prefijos propios: {Prefijos_Propios_W2}")
print("")
print(f"Sufijos propios: {Sufijos_Propios_W2}")
print("")
print(f"Subcadenas: {Subcadenas_W2}")
print("")
print(f"Subcaenas propias: {Subcadenas_Propias_W2}")
print("")
print(f"Subsecuencias: {Subsecuencias_W2}")