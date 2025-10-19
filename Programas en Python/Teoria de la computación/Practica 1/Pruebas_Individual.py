import random # Módulo necesario para generar los lenguajes aleatorios

# Función para generar los lenguajes a partir del diccionario
def Lenguajes(Diccionario):
    Long_Diccionario = len(Diccionario)
    print("")
    Numero_Elementos = int(input("Ingresa la cantidad de elementos de los lenguajes a generar (debe ser menor o igual al # de elementos en el alfabeto): "))

    if Numero_Elementos > len(Diccionario) or Numero_Elementos <= 0:
        print("")
        print("-----Número de elementos fuera de rango, intente de nuevo")
        
        Lenguaje_1 = "-----El lenguaje 1 no se pudo generar-----" 
        Lenguaje_2 = "-----El lenguaje 2 no se pudo generar-----"

        return Lenguaje_1,Lenguaje_2
    else:
        Long_Elemento = int(input("Ingresa la longitud que va a tener cada elemento de los lenguajes: "))
        Lenguaje_1 = []
        Lenguaje_2 = []
        S_Aux = ""

        for Iteracion in range(0,2):
            # Genera número aleatorios sin que se repitan mediante un rango
            Numeros_aleatorios = random.sample(range(0,Long_Diccionario),Numero_Elementos) 

            # Genera los elementos aleatorios
            for Indice in range(0,Numero_Elementos):
                for Indice2 in range(0,Long_Elemento):
                    # Genera números aleatorios mediante un rango, pero se pueden repetir
                    Elemento_Aleatorio = random.randint(0,Long_Diccionario)

                    if Elemento_Aleatorio == Long_Diccionario:
                        w = 0
                    else:
                        if Long_Elemento == 1:
                            print("Hola1")
                            S_Aux = S_Aux + Diccionario[Numeros_aleatorios[Indice]]
                        else:
                            print("Hola2")
                            S_Aux = S_Aux + Diccionario[Elemento_Aleatorio]

                # Condiciones para los lenguajes
                if Iteracion == 0:
                    # Agrega los elementos al Lenguaje_1
                    if len(S_Aux) == Long_Elemento:
                        Lenguaje_1.append(S_Aux)
                    elif len(S_Aux) < Long_Elemento:
                        if Long_Elemento == 1:
                            S_Aux = S_Aux + Diccionario[Numeros_aleatorios[Indice]]
                            Lenguaje_1.append(S_Aux)
                        else:
                            i = 0
                            while i < (Long_Elemento - len(S_Aux)):
                                if Elemento_Aleatorio == 0:
                                    S_Aux = S_Aux + Diccionario[Elemento_Aleatorio + 1]
                                else:
                                    S_Aux = S_Aux + Diccionario[Elemento_Aleatorio - 1]
                            Lenguaje_1.append(S_Aux)
                    S_Aux = ""
                else:
                    # Agrega los elementos al Lenguaje_2
                    if len(S_Aux) == Long_Elemento:
                        Lenguaje_2.append(S_Aux)
                    elif len(S_Aux) < Long_Elemento:
                        if Long_Elemento == 1:
                            S_Aux = S_Aux + Diccionario[Numeros_aleatorios[Indice]]
                            Lenguaje_2.append(S_Aux)
                        else:
                            i = 0
                            while i < (Long_Elemento - len(S_Aux)):
                                if Elemento_Aleatorio == 0:
                                    S_Aux = S_Aux + Diccionario[Elemento_Aleatorio + 1]
                                else:
                                    S_Aux = S_Aux + Diccionario[Elemento_Aleatorio - 1]
                            Lenguaje_2.append(S_Aux)
                    S_Aux = ""
        
        return Lenguaje_1,Lenguaje_2
    

Diccionario = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

l1,l2 = Lenguajes(Diccionario)

print(l1)
print(l2)