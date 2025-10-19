# Práctica 1: Alfabetos, lenguajes y expresiones regulares
# Integrantes: García Escamilla Bryan Alexis y Melendez Macedonio Rodrigo

import re # Módulo necesario

# Función que evalua una cadena de caracteres
def Expresion_Regular():
    Palabra = input("Ingrese una palabra: ")
    R = "bcdfghjklmnñpqrstvwxyz"

    Expresion_Regular = fr"^(([{R}]?)+(a)(a|[{R}]?)+(e)(e|[{R}]?)+(i)(i|[{R}]?)+(o)(o|[{R}]?)+(u)(u|[{R}]?)+)+$"
    Resultado = re.search(Expresion_Regular,Palabra)

    return Resultado

while True:
    Resultado = Expresion_Regular()

    if Resultado == None:
        print("")
        print("-----La palabra es incorrecta!-----")
        print("")
    else:
        print("")
        print("-----La palabra es correcta!-----")
        print("")