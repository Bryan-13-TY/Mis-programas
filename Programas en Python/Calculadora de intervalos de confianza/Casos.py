"""
Parámetros a estimar.

Este archivo contiene las funciones para cada uno de los parámetros a estimar en donde se piden los datos correspondientes.

Autor: García Escamilla Bryan Alexis
Fecha: 16/08/2025
"""

from Calculos import ICCaso1, ICCaso2, ICCaso3, ICCaso4, ICCaso5, ICCaso6, ICCaso7, ICCaso8, ICCaso9, ICCaso10 # Necesarias para los calculos
from Calculos import FormatoMuest, CantidadMuest, FloatInt
from Graficas import GraficarIC_ZC1, GraficarIC_TC2, GraficarIC_ZC3, GraficarIC_ZC4, GraficarIC_TC5, GraficarIC_TC6, GraficarIC_ZC7, GraficarIC_ZC8, GraficarIC_XC9, GraficarIC_FC10 # Necesarias para las gráficas

BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_WHITE = "\033[97m"
RESET = "\033[0m"

def MediaPoblacional(RutaIMG1: str, RutaIMG2: str):
    """
    Para estimar una media poblacional.

    Esta función considera las dos situaciones para estimar una media poblacional:

    - Distribución normal, muestra grande y varianza conocida.
    - Distribución normal, muestra grande y varianza desconocida.

    Para cada una se piden y se calculan los datos necesarios para obtener el intervalo de confianza. 

    Parameters
    ----------
    RutaIMG1 : str
        Ruta de la imagen de la fórmula del intervalo de confianza para el caso 1.
    RutaIMG2 : str
        Ruta de la imagen de la fórmula del intervalo de confianza para el caso 2.
    """
    TMuest = input("Escribe el tamaño de la muestra (n): ")
    if TMuest.isdigit() and int(TMuest) >= 1:
        Muest = input(f"\nEscribe las {TMuest} observaciones (x₁ x₂ ... xₙ): ")
        if FormatoMuest(Muest): # Se valida el formato de las observaciones
            if CantidadMuest(Muest, TMuest): # Se valida la cantidad de observaciones
                PConf = input("\nEscribe el porcentaje (%) de confianza: ")
                if PConf.isdigit() and 0 < int(PConf) <= 100:
                    # Mostrar mensajes de advertencia
                    if int(PConf) < 90:
                        print(f"{BRIGHT_YELLOW}>> ⚠️ Usar un nivel de confianza menor a 90% implica un mayor riesgo de que el intervalo no contenga el valor real. Se recomienda 90% o más.{RESET}")
                    elif int(PConf) == 100:
                        print(f"{BRIGHT_YELLOW}>> ⚠️ Un nivel de confianza del 100% genera un intervalo demasiado amplio y poco útil. Se recomienda usar 90%, 95% o 99%.{RESET}")

                    EstVar = input("\n¿La varianza poblacional (σ²) es conocida (si / no)? ")

                    match (EstVar.strip()).upper():
                        case "SI":
                            DesEstPob = input("\nEscribe el valor de la desviación estándar poblacional (σ): ")
                            if FloatInt(DesEstPob): # Saber si es un entero o decimal
                                if float(DesEstPob) >= 0:
                                    print(f"\n{BRIGHT_YELLOW}>> Los datos corresponden al caso 1{RESET}")
                                    print(f"\n{BRIGHT_MAGENTA}- Parámetro a estimar: μ{RESET}")
                                        
                                    if int(TMuest) >= 30: # Muestra grande
                                        print(f"{BRIGHT_MAGENTA}- Situación: Distribución normal, muestra grande y varianza conocida.{RESET}")
                                    else: # Muestra pequeña
                                        print(f"{BRIGHT_MAGENTA}- Situación: Distribución normal, muestra pequeña y varianza conocida.{RESET}")
                                        
                                    print(f"{BRIGHT_MAGENTA}- Estimador puntual: X̄{RESET}")

                                    # Recuperamos los datos de la función
                                    Intervalo, Media, LitSup, LitInf = ICCaso1(Muest, TMuest, float(DesEstPob), PConf)

                                    # Se imprime el resultado
                                    print(f"\n{BRIGHT_GREEN}>> ✅ El intervalo de confianza para la media muestral X̄ = {Media} es: {Intervalo}{RESET}")

                                    if int(TMuest) >= 30: # Muestra grande
                                        GraficarIC_ZC1(Media, LitSup, LitInf, float(DesEstPob), float(TMuest), f"Intervalo de confianza al {PConf}% para μ (muestra grande y varianza conocida)\nX̄ = {Media}, n = {TMuest}, σ = {DesEstPob}", PConf, RutaIMG1)
                                    else:
                                        GraficarIC_ZC1(Media, LitSup, LitInf, float(DesEstPob), float(TMuest), f"Intervalo de confianza al {PConf}% para μ (muestra pequeña y varianza conocida)\nX̄ = {Media}, n = {TMuest}, σ = {DesEstPob}", PConf, RutaIMG1)
                                else:
                                    print(f"{BRIGHT_RED}>> ❌ La desviación estándar poblacional debe ser mayor o igual a cero.")
                            else:
                                print(f"{BRIGHT_RED}>> ❌ La varianza poblacional debe ser un número.{RESET}")
                        case "NO":
                            print(f"\n{BRIGHT_YELLOW}>> Los datos corresponden al caso 2{RESET}")
                            print(f"\n{BRIGHT_MAGENTA}- Parámetro a estimar: μ{RESET}")

                            if int(TMuest) >= 30: # Muestra grande
                                print(f"{BRIGHT_MAGENTA}- Situación: Distribución normal, muestra grande y varianza desconocida.{RESET}")
                            else: # Muestra pequeña
                                print(f"{BRIGHT_MAGENTA}- Situación: Distribución normal, muestra pequeña y varianza desconocida.{RESET}")

                            print(f"{BRIGHT_MAGENTA}- Estimador puntual: X̄{RESET}")

                            # Recuperamos los datos de la función
                            Intervalo, Media, LitSup, LitInf, S = ICCaso2(Muest, TMuest, PConf)

                            # Se imprime el resultado
                            print(f"\n{BRIGHT_GREEN}>> ✅ El intervalo de confianza para la media muestral X̄ = {Media} es: {Intervalo}{RESET}")
                                
                            if int(TMuest) >= 30: # Muestra grande
                                 GraficarIC_TC2(Media, LitSup, LitInf, S, float(TMuest), f"Intervalo de confianza al {PConf}% para μ (muestra grande y varianza desconocida)\nX̄ = {Media}, n = {TMuest}", PConf, RutaIMG2)
                            else: # Muestra pequeña
                                GraficarIC_TC2(Media, LitSup, LitInf, S, float(TMuest), f"Intervalo de confianza al {PConf}% para μ (muestra pequeña y varianza desconocida)\nX̄ = {Media}, n = {TMuest}", PConf, RutaIMG2)
                        case _:
                            print(f"{BRIGHT_RED}>> ❌ La entrada no es válida.{RESET}")
                else:
                    print(f"{BRIGHT_RED}>> ❌ El porcentaje debe ser un número entero mayor que cero y menor o igual a 100.{RESET}")
            else:
                print(f"{BRIGHT_RED}>> ❌ El número de observaciones no coincide con el tamaño de la muestra (n).{RESET}")
        else:
            print(f"{BRIGHT_RED}>> ❌ El formato de las observaciones no es correcto.{RESET}")
    else:
        print(f"{BRIGHT_RED}>> ❌ El tamaño de la muestra debe ser un número entero mayor o igual a 1.{RESET}")

def DifMediaPoblacional(RutaIMG3: str, RutaIMG4: str, RutaIMG5: str, RutaIMG6: str):
    """
    Para estimar una diferencia de medias poblacionales.

    Esta función considera las cuatros situaciones para estimar una diferencia de medias poblacionales:

    - Para dos muestras independientes de poblaciones normales con varianzas conocidas.
    - Para dos muestras grandes (n > 30) independientes de poblaciones normales con varianzas diferentes y desconocidas.
    - Para dos muestras chicas independientes de poblaciones normales con varianzas diferentes y desconocidas.
    - Para dos muestras independientes de poblaciones normales con varianzas iguales y desconocidas.

    Para cada una se piden y se calculan los datos necesarios para obtener el intervalo de confianza. 

    Parameters
    ----------
    RutaIMG3 : str
        Ruta de la imagen de la fórmula del intervalo de confianza para la situación 1.
    RutaIMG4 : str
        Ruta de la imagen de la fórmula del intervalo de confianza para la situación 2.
    RutaIMG5 : str
        Ruta de la imagan de la fórmula del intervalo de confianza para la situación 3.
    RutaIMG6 : str
        Ruta de la imagen de la fórmula del intervalo de confianza para la situación 4.
    """
    TMuest = input("Escribe el tamaño de la muestra (n): ")
    TMuest1 = input("Escribe el tamaño de la muestra (n₁): ")
    if TMuest1.isdigit() and int(TMuest1) >= 1:
        Muest1 = input(f"\nEscribe las {TMuest1} observaciones (x₁ x₂ ... xₙ): ")
        if FormatoMuest(Muest1): # Se valida el formato de las observaciones
            if CantidadMuest(Muest1, TMuest1): # Se valida la cantidad de observaciones
                TMuest2 = input("\nEscribe el tamaño de la muestra (n₂): ")
                if TMuest2.isdigit() and int(TMuest2) >= 1:
                    Muest2 = input(f"\nEscribe las {TMuest2} observaciones (x₁ x₂ ... xₙ): ")
                    if FormatoMuest(Muest2): # Se valida el formato de las observaciones
                        if CantidadMuest(Muest2, TMuest2): # Se valida la cantidad de observaciones
                            PConf = input("\nEscribe el porcentaje (%) de confianza: ")
                            if PConf.isdigit() and 0 < int(PConf) <= 100:
                                # Mostrar mensajes de advertencia
                                if int(PConf) < 90:
                                    print(f"{BRIGHT_YELLOW}>> ⚠️ Usar un nivel de confianza menor a 90% implica un mayor riesgo de que el intervalo no contenga el valor real. Se recomienda 90% o más.{RESET}")
                                elif int(PConf) == 100:
                                    print(f"{BRIGHT_YELLOW}>> ⚠️ Un nivel de confianza del 100% genera un intervalo demasiado amplio y poco útil. Se recomienda usar 90%, 95% o 99%.{RESET}")
                                
                                EstVar = input("\n¿Las varianzas poblacionales (σ₁ y σ₂) son conocidas (si / no)? ")

                                match (EstVar.strip()).upper():
                                    case "SI":
                                        DesEstPob1 = input("\nEscribe el valor de la desviación estándar poblacional (σ₁): ")
                                        if FloatInt(DesEstPob1): # Saber si es un entero o decimal
                                            if float(DesEstPob1) >= 0:
                                                DesEstPob2 = input("\nEscribe el valor de la desviación estándar poblacional (σ₂): ")
                                                if FloatInt(DesEstPob2): # Saber si es un entero o decimal
                                                    if float(DesEstPob2) >= 0:
                                                        print(f"\n{BRIGHT_YELLOW}>> Los datos corresponden al caso 3{RESET}")
                                                        print(f"\n{BRIGHT_MAGENTA}- Parámetro a estimar: μ₁ - μ₂{RESET}")
                                                        print(f"{BRIGHT_MAGENTA}- Situación: Para dos muestras independientes de poblaciones normales con varianzas conocidas.{RESET}")
                                                        print(f"{BRIGHT_MAGENTA}- Estimador puntual: X̄₁ - X̄₂{RESET}")

                                                        # Recuperamos los datos de la función
                                                        Intervalo, DifMedia, LitSup, LitInf = ICCaso3(Muest1, Muest2, float(DesEstPob1), float(DesEstPob2), TMuest1, TMuest2, PConf)

                                                        # Se imprime el resultado
                                                        print(f"\n{BRIGHT_GREEN}>> ✅ El intervalo de confianza para la diferencia de medias muestrales X̄₁ - X̄₂ = {DifMedia} es: {Intervalo}{RESET}")
                                                        GraficarIC_ZC3(DifMedia, LitSup, LitInf, f"Intervalo de confianza al {PConf}% para μ₁ - μ₂ (dos muestras independientes de poblaciones normales con varianzas conocidas)\nX̄₁ - X̄₂ = {DifMedia}, n₁ = {TMuest1}, n₂ = {TMuest2}, σ₁ = {DesEstPob1}, σ₂ = {DesEstPob2}", PConf, RutaIMG3)
                                                    else:
                                                        print(f"{BRIGHT_RED}>> ❌ La desviación estándar poblacional debe ser mayor o igual a cero.")
                                                else:
                                                    print(f"{BRIGHT_RED}>> ❌ La varianza poblacional debe ser un número.{RESET}")
                                            else:
                                                print(f"{BRIGHT_RED}>> ❌ La desviación estándar poblacional debe ser mayor o igual a cero.")
                                        else:
                                            print(f"{BRIGHT_RED}>> ❌ La varianza poblacional debe ser un número.{RESET}")
                                    case "NO":
                                        EstVar2 = input("\n¿Las varianzas poblacionales (σ₁ y σ₂) son diferentes (si / no / no se)? ")

                                        match (EstVar2.strip()).upper(): # Se determina si las varianzas poblaciones son iguales o diferenteso se desconoce
                                            case "SI":
                                                if (int(TMuest1) >= 30) and (int(TMuest2) >= 30): # Dos muestras grandes
                                                    print(f"\n{BRIGHT_YELLOW}>> Los datos corresponden al caso 4{RESET}")
                                                    print(f"\n{BRIGHT_MAGENTA}- Parámetro a estimar: μ₁ - μ₂{RESET}")
                                                    print(f"{BRIGHT_MAGENTA}- Situación: Para dos muestras grandes (n > 30) independientes de poblaciones normales con varianzas diferentes y desconocidas.{RESET}")
                                                    print(f"{BRIGHT_MAGENTA}- Estimador puntual: X̄₁ - X̄₂{RESET}")

                                                    # Recuperamos los datos de la función
                                                    Intervalo, DifMedia, LitSup, LitInf, Z = ICCaso4(Muest1, Muest2, TMuest1, TMuest2, PConf)

                                                    # Se imprime el resultado
                                                    print(f"\n{BRIGHT_GREEN}>> ✅ El intervalo de confianza para la diferencia de medias muestrales X̄₁ - X̄₂ = {DifMedia} es: {Intervalo}{RESET}")
                                                    GraficarIC_ZC4(DifMedia, LitSup, LitInf, Z, f"Intervalo de confianza al {PConf}% para μ₁ - μ₂ (dos muestras grandes (n > 30) independientes de poblaciones normales con varianzas diferentes y desconocidas)\nX̄₁ - X̄₂ = {DifMedia}, n₁ = {TMuest1}, n₂ = {TMuest2}", PConf, RutaIMG4)
                                                elif (int(TMuest1) < 30) and (int(TMuest2) < 30): # Dos muestras pequeñas
                                                    print(f"\n{BRIGHT_YELLOW}>> Los datos corresponden al caso 5{RESET}")
                                                    print(f"\n{BRIGHT_MAGENTA}- Parámetro a estimar: μ₁ - μ₂{RESET}")
                                                    print(f"{BRIGHT_MAGENTA}- Situación: Para dos muestras chicas independientes de poblaciones normales con varianzas diferentes y desconocidas.{RESET}")
                                                    print(f"{BRIGHT_MAGENTA}- Estimador puntual: X̄₁ - X̄₂{RESET}")

                                                    # Recuperamos los datos de la función
                                                    Intervalo, DifMedia, LitSup, LitInf, T, Gl = ICCaso5(Muest1, Muest2, TMuest1, TMuest2, PConf)

                                                    # Se imprime el resultado
                                                    print(f"\n{BRIGHT_GREEN}>> ✅ El intervalo de confianza para la diferencia de medias muestrales X̄₁ - X̄₂ = {DifMedia} es: {Intervalo}{RESET}")
                                                    GraficarIC_TC5(DifMedia, LitSup, LitInf, T, Gl, f"Intervalo de confianza al {PConf}% para μ₁ - μ₂ (dos muestras chicas independientes de poblaciones normales con varianzas diferentes y desconocidas)\nX̄₁ - X̄₂ = {DifMedia}, n₁ = {TMuest1}, n₂ = {TMuest2}", PConf, RutaIMG5)
                                            case "NO":
                                                print(f"\n{BRIGHT_YELLOW}>> Los datos corresponden al caso 6{RESET}")
                                                print(f"\n{BRIGHT_MAGENTA}- Parámetro a estimar: μ₁ - μ₂{RESET}")
                                                print(f"{BRIGHT_MAGENTA}- Situación: Para dos muestras independientes de poblaciones normales con varianzas iguales y desconocidas.{RESET}")
                                                print(f"{BRIGHT_MAGENTA}- Estimador puntual: X̄₁ - X̄₂{RESET}")

                                                # Recuperamos los datos de la función
                                                Intervalo, DifMedia, LitSup, LitInf, T, Gl = ICCaso6(Muest1, Muest2, TMuest1, TMuest2, PConf)

                                                # Se imprime el resultado
                                                print(f"\n{BRIGHT_GREEN}>> ✅ El intervalo de confianza para la diferencia de medias X̄₁ - X̄₂ = {DifMedia} es: {Intervalo}{RESET}")
                                                GraficarIC_TC6(DifMedia, LitSup, LitInf, T, Gl, f"Intervalo de confianza al {PConf}% para μ₁ - μ₂ (dos muestras independientes de poblaciones normales con varianzas iguales y desconocidas)\nX̄₁ - X̄₂ = {DifMedia}, n₁ = {TMuest1}, n₂ = {TMuest2}", PConf, RutaIMG6)
                                            case "NO SE":
                                                print(f"\n{BRIGHT_BLUE}Dado que no se conocen las varianzas poblacionales se requiere averiguar si éstas son estadísticamente diferentes o no. Para ello construimos el intervalo de confianza para el cociente de las varianzas poblacionales (σ₁² / σ₂²), si tal intervalo contiene al 1 se concluye que las varianzas aunque desconocidas se pueden considerar estadísticamente iguales.{RESET}")
                                                Intervalo, EstVar3, *_ = ICCaso10(Muest1, Muest2, TMuest1, TMuest2, PConf)

                                                # Se determian si las varianzas son iguales o diferentes, de acuerdo con el intervalo del cociente de varianzas
                                                match EstVar3:
                                                    case "NO": # Las varianzas poblacionales son estadísticamente diferentes
                                                        print(f"\n{BRIGHT_BLUE}>> El intervalo resultante es {Intervalo} en donde el 1 {EstVar3} se encuentra, entonces las varianzas poblacionales se consideran estadísticamente diferentes{RESET}")
                                                        
                                                        if (int(TMuest1) >= 30) and (int(TMuest2) >= 30): # Dos muestras grandes
                                                            print(f"\n{BRIGHT_YELLOW}>> Los datos corresponden al caso 4{RESET}")
                                                            print(f"\n{BRIGHT_MAGENTA}- Parámetro a estimar: μ₁ - μ₂{RESET}")
                                                            print(f"{BRIGHT_MAGENTA}- Situación: Para dos muestras grandes (n > 30) independientes de poblaciones normales con varianzas diferentes y desconocidas.{RESET}")
                                                            print(f"{BRIGHT_MAGENTA}- Estimador puntual: X̄₁ - X̄₂{RESET}")

                                                            # Recuperamos los datos de la función
                                                            Intervalo, DifMedia, LitSup, LitInf, Z = ICCaso4(Muest1, Muest2, TMuest1, TMuest2, PConf)

                                                            # Se imprime el resultado
                                                            print(f"\n{BRIGHT_GREEN}>> ✅ El intervalo de confianza para la diferencia de medias muestrales X̄₁ - X̄₂ = {DifMedia} es: {Intervalo}{RESET}")
                                                            GraficarIC_ZC4(DifMedia, LitSup, LitInf, Z, f"Intervalo de confianza al {PConf}% para μ₁ - μ₂ (dos muestras grandes (n > 30) independientes de poblaciones normales con varianzas diferentes y desconocidas)\nX̄₁ - X̄₂ = {DifMedia}, n₁ = {TMuest1}, n₂ = {TMuest2}", PConf, RutaIMG4)
                                                        elif (int(TMuest1) < 30) and (int(TMuest2) < 30): # Dos muestras pequeñas
                                                            print(f"\n{BRIGHT_YELLOW}>> Los datos corresponden al caso 5{RESET}")
                                                            print(f"\n{BRIGHT_MAGENTA}- Parámetro a estimar: μ₁ - μ₂{RESET}")
                                                            print(f"{BRIGHT_MAGENTA}- Situación: Para dos muestras chicas independientes de poblaciones normales con varianzas diferentes y desconocidas.{RESET}")
                                                            print(f"{BRIGHT_MAGENTA}- Estimador puntual: X̄₁ - X̄₂{RESET}")

                                                            # Recuperamos los datos de la función
                                                            Intervalo, DifMedia, LitSup, LitInf, T, Gl = ICCaso5(Muest1, Muest2, TMuest1, TMuest2, PConf)

                                                            # Se imprime el resultado
                                                            print(f"\n{BRIGHT_GREEN}>> ✅ El intervalo de confianza para la diferencia de medias muestrales X̄₁ - X̄₂ = {DifMedia} es: {Intervalo}{RESET}")
                                                            GraficarIC_TC5(DifMedia, LitSup, LitInf, T, Gl, f"Intervalo de confianza al {PConf}% para μ₁ - μ₂ (dos muestras chicas independientes de poblaciones normales con varianzas diferentes y desconocidas)\nX̄₁ - X̄₂ = {DifMedia}, n₁ = {TMuest1}, n₂ = {TMuest2}", PConf, RutaIMG5)
                                                    case "SI": # Las varianzas son estadísticamente iguales
                                                        print(f"\n{BRIGHT_BLUE}>> El intervalo resultante es {Intervalo} en donde el 1 {EstVar3} se encuentra, entonces las varianzas poblacionales se consideran estadísticamente iguales{RESET}")

                                                        print(f"\n{BRIGHT_YELLOW}>> Los datos corresponden al caso 6{RESET}")
                                                        print(f"\n{BRIGHT_MAGENTA}- Parámetro a estimar: μ₁ - μ₂{RESET}")
                                                        print(f"{BRIGHT_MAGENTA}- Situación: Para dos muestras independientes de poblaciones normales con varianzas iguales y desconocidas.{RESET}")
                                                        print(f"{BRIGHT_MAGENTA}- Estimador puntual: X̄₁ - X̄₂{RESET}")

                                                        # Recuperamos los datos de la función
                                                        Intervalo, DifMedia, LitSup, LitInf, T, Gl = ICCaso6(Muest1, Muest2, TMuest1, TMuest2, PConf)

                                                        # Se imprime el resultado
                                                        print(f"\n{BRIGHT_GREEN}>> ✅ El intervalo de confianza para la diferencia de medias X̄₁ - X̄₂ = {DifMedia} es: {Intervalo}{RESET}")
                                                        GraficarIC_TC6(DifMedia, LitSup, LitInf, T, Gl, f"Intervalo de confianza al {PConf}% para μ₁ - μ₂ (dos muestras independientes de poblaciones normales con varianzas iguales y desconocidas)\nX̄₁ - X̄₂ = {DifMedia}, n₁ = {TMuest1}, n₂ = {TMuest2}", PConf, RutaIMG6)
                                            case _:
                                                print(f"{BRIGHT_RED}>> ❌ La entrada no es válida.{RESET}")
                                    case _:
                                        print(f"{BRIGHT_RED}>> ❌ La entrada no es válida.{RESET}")
                            else:
                                print(f"{BRIGHT_RED}>> ❌ El porcentaje debe ser un número entero mayor que cero y menor o igual a 100.{RESET}")
                        else:
                            print(f"{BRIGHT_RED}>> ❌ El número de observaciones no coincide con el tamaño de la muestra (n₁).{RESET}")
                    else:
                        print(f"{BRIGHT_RED}>> ❌ El formato de las observaciones no es correcto.{RESET}")
                else:
                    print(f"{BRIGHT_RED}>> ❌ El tamaño de la muestra debe ser un número entero mayor o igual a 1.{RESET}")
            else:
                print(f"{BRIGHT_RED}>> ❌ El número de observaciones no coincide con el tamaño de la muestra (n₂).{RESET}")
        else:
            print(f"{BRIGHT_RED}>> ❌ El formato de las observaciones no es correcto.{RESET}")
    else:
        print(f"{BRIGHT_RED}>> ❌ El tamaño de la muestra debe ser un número entero mayor o igual a 1.{RESET}")

def Proporcion(RutaIMG7: str):
    """
    Para estimar una proporción.

    Esta función considera la única situación para estimar una proporción:

    - Para una muestra grande con 𝑃 pequeña.

    Para ello se pide y se calculan los datos necesarios para obtener el intervalo de confianza. 

    Parameters
    ----------
    RutaIMG7 : str
        Ruta de la imagen de la fórmula del intervalo de confianza para la única situación.
    """
    TMuest = input("Escribe el tamaño de la muestra (N): ")
    if TMuest.isdigit() and int(TMuest) >= 1:
        NoExit = input("\nEscribe el número de éxitos (X): ")
        if NoExit.isdigit() and 1 <= int(NoExit) <= int(TMuest):
            PConf = input("\nEscribe el porcentaje (%) de confianza: ")
            if PConf.isdigit() and 0 < int(PConf) <= 100:
                # Mostrar mensajes de advertencia
                if int(PConf) < 90:
                    print(f"{BRIGHT_YELLOW}>> ⚠️ Usar un nivel de confianza menor a 90% implica un mayor riesgo de que el intervalo no contenga el valor real. Se recomienda 90% o más.{RESET}")
                elif int(PConf) == 100:
                    print(f"{BRIGHT_YELLOW}>> ⚠️ Un nivel de confianza del 100% genera un intervalo demasiado amplio y poco útil. Se recomienda usar 90%, 95% o 99%.{RESET}")

                if (int(TMuest) * (int(NoExit) / int(TMuest))) >= 5 and (int(TMuest) * (1 - (int(NoExit) / int(TMuest)))) >= 5: # Se cumple la condición para usar la normal
                    print(f"\n{BRIGHT_YELLOW}>> Los datos corresponden al caso 7{RESET}")
                    print(f"\n{BRIGHT_MAGENTA}- Parámetro a estimar: 𝑃{RESET}")
                    print(f"{BRIGHT_MAGENTA}- Situación: Para una muestra grande con 𝑃 pequeña.{RESET}")
                    print(f"{BRIGHT_MAGENTA}- Estimador puntual: 𝑝{RESET}")

                    # Recuperamos los datos de la función
                    Intervalo, p, LitSup, LitInf, Z = ICCaso7(NoExit, TMuest, PConf)

                    # Se imprime el resultado
                    print(f"\n{BRIGHT_GREEN}>> ✅ El intervalo de confianza para la proporción p = {p} es: {Intervalo}{RESET}")
                    GraficarIC_ZC7(p, LitSup, LitInf, Z, f"Intervalo de confianza al {PConf}% para P (muestra grande con P pequeña)\n X = {NoExit}, N = {TMuest}, p = {p}", PConf, RutaIMG7)
                else:
                    print(f"{BRIGHT_YELLOW}>> ⚠️ No se puede usar la aproximación normal porque no se cumplen con las condiciones np >= 5 y n(1-p) >= 5. Usa un método exacto o corregido.{RESET}")
            else:
                print(f"{BRIGHT_RED}>> ❌ El porcentaje debe ser un número entero mayor que cero y menor o igual a 100.{RESET}")
        else:
            print(f"{BRIGHT_RED}>> ❌ El número de éxitos debe ser mayor o igual a 1 y menor o igual al tamaño de la muestra.{RESET}")
    else:
        print(f"{BRIGHT_RED}>> ❌ El tamaño de la muestra debe ser un número entero mayor o igual a 1.{RESET}")

def DifProporcion(RutaIMG8: str):
    """
    Para estimar una diferencia de proporciones.

    Esta función considera la única situación para estimar una diferecia de proporciones:

    - Para dos muestras grandes e independientes de una distribución normal.

    Para ello se pide y se calculan los datos necesarios para obtener el intervalo de confianza. 

    Parameters
    ----------
    RutaIMG8 : str
        Ruta de la imagen de la fórmula del intervalo de confianza para la única situación.
    """
    TMuest1 = input("Escribe el tamaño de la muestra (N₁): ")
    if TMuest1.isdigit() and int(TMuest1) >= 1:
        NoExit1 = input("\nEscribe el número de éxitos (X₁): ")
        if NoExit1.isdigit() and 1 <= int(NoExit1) <= int(TMuest1):
            TMuest2 = input("\nEscribe el tamaño de la muestra (N₂): ")
            if TMuest2.isdigit() and int(TMuest2) >= 1:
                NoExit2 = input("\nEscribe el número de éxitos (X₂): ")
                if NoExit2.isdigit() and 1 <= int(NoExit2) <= int(TMuest2):
                    PConf = input("\nEscribe el porcentaje (%) de confianza: ")
                    if PConf.isdigit() and 0 < int(PConf) <= 100:
                        # Mostrar mensajes de advertencia
                        if int(PConf) < 90:
                            print(f"{BRIGHT_YELLOW}>> ⚠️ Usar un nivel de confianza menor a 90% implica un mayor riesgo de que el intervalo no contenga el valor real. Se recomienda 90% o más.{RESET}")
                        elif int(PConf) == 100:
                            print(f"{BRIGHT_YELLOW}>> ⚠️ Un nivel de confianza del 100% genera un intervalo demasiado amplio y poco útil. Se recomienda usar 90%, 95% o 99%.{RESET}")

                        if (int(TMuest1) * (int(NoExit1) / int(TMuest1))) >= 5 and (int(TMuest1) * (1 - (int(NoExit1) / int(TMuest1)))) >= 5 and (int(TMuest2) * (int(NoExit2) / int(TMuest2))) >= 5 and (int(TMuest2) * (1 - (int(NoExit2) / int(TMuest2)))) >= 5:
                            print(f"\n{BRIGHT_YELLOW}>> Los datos corresponden al caso 8{RESET}")
                            print(f"\n{BRIGHT_MAGENTA}- Parámetro a estimar: 𝑃₁ - 𝑃₂{RESET}")
                            print(f"{BRIGHT_MAGENTA}- Situación: Para dos muestras grandes e independientes de una distribución normal.{RESET}")
                            print(f"{BRIGHT_MAGENTA}- Estimador puntual: 𝑝₁ - 𝑝₂{RESET}")

                            # Recuperamos los datos de la función
                            Intervalo, Difp, LitSup, LitInf, Z = ICCaso8(NoExit1, NoExit2, TMuest1, TMuest2, PConf)

                            # Se imprime el resultado
                            print(f"\n{BRIGHT_GREEN}>> ✅ El intervalo de confianza para la diferencia de proporciones p₁ - p₂ = {Difp} es: {Intervalo}{RESET}")
                            GraficarIC_ZC8(Difp, LitSup, LitInf, Z, f"Intervalo de confianza al {PConf}% para P₁ - P₂ (dos muestras grandes e independientes de una distribución normal)\n X₁ = {NoExit1}, N₁ = {TMuest1}, X₂ = {NoExit2}, N₂ = {TMuest2}, p₁ - p₂ = {Difp}", PConf, RutaIMG8)
                        else:
                            print(f"{BRIGHT_YELLOW}>> ⚠️ No se puede usar la aproximación normal para la diferencia de proporciones porque alguna de las muestras no cumple con las condiciones de normalidad: np >= 5 y n(1-p) >= 5. Usa un método exacto o corregido{RESET}")
                    else:
                        print(f"{BRIGHT_RED}>> ❌ El porcentaje debe ser un número entero mayor que cero y menor o igual a 100.{RESET}")
                else:
                    print(f"{BRIGHT_RED}>> ❌ El número de éxitos debe ser mayor o igual a 1 y menor o igual al tamaño de la muestra.{RESET}")
            else:
                print(f"{BRIGHT_RED}>> ❌ El tamaño de la muestra debe ser un número entero mayor o igual a 1.{RESET}")   
        else:
            print(f"{BRIGHT_RED}>> ❌ El número de éxitos debe ser mayor o igual a 1 y menor o igual al tamaño de la muestra.{RESET}")
    else:
        print(f"{BRIGHT_RED}>> ❌ El tamaño de la muestra debe ser un número entero mayor o igual a 1.{RESET}")

def VarianzaPoblacional(RutaIMG9: str):
    """
    Para estimar una varianza poblacional.

    Esta función considera la única situación para estimar una varianza poblacional:

    - Para una muestra cualquiera.

    Para ello se pide y se calculan los datos necesarios para obtener el intervalo de confianza. 

    Parameters
    ----------
    RutaIMG9 : str
        Ruta de la imagen de la fórmula del intervalo de confianza para la única situación.
    """
    TMuest = input("Escribe el tamaño de la muestra (n): ")
    if TMuest.isdigit() and int(TMuest) >= 1:
        Muest = input(f"\nEscribe las {TMuest} observaciones (x₁ x₂ ... xₙ): ")
        if FormatoMuest(Muest): # Se vaida el formato de las observaciones
            if CantidadMuest(Muest, TMuest): # Se valida la cantidad de observaciones
                PConf = input("\nEscribe el porcentaje (%) de confianza: ")
                if PConf.isdigit() and 0 < int(PConf) <= 100:
                    # Mostrar mensajes de advertencia
                    if int(PConf) < 90:
                        print(f"{BRIGHT_YELLOW}>> ⚠️ Usar un nivel de confianza menor a 90% implica un mayor riesgo de que el intervalo no contenga el valor real. Se recomienda 90% o más.{RESET}")
                    elif int(PConf) == 100:
                        print(f"{BRIGHT_YELLOW}>> ⚠️ Un nivel de confianza del 100% genera un intervalo demasiado amplio y poco útil. Se recomienda usar 90%, 95% o 99%.{RESET}")

                    print(f"\n{BRIGHT_YELLOW}>> Los datos corresponden al caso 9{RESET}")
                    print(f"\n{BRIGHT_MAGENTA}- Parámetro a estimar: σ²{RESET}")
                    print(f"{BRIGHT_MAGENTA}- Situación: Para una muestra cualquiera.{RESET}")
                    print(f"{BRIGHT_MAGENTA}- Estimador puntual: 𝑠²{RESET}")

                    # Recuperamos los datos de la función
                    Intervalo, S, LitSup, LitInf, Gl = ICCaso9(Muest, TMuest, PConf)

                    # Se imprime el resultado
                    print(f"\n{BRIGHT_GREEN}>> ✅ El intervalo de confianza para la varianza muestral es 𝑠² = {S} es: {Intervalo}{RESET}")
                    GraficarIC_XC9(S, LitSup, LitInf, Gl, f"Intervalo de confianza al {PConf}% para σ² (una muestra cualquiera)\nn = {TMuest}, S² = {S}", PConf, RutaIMG9)
                else:
                    print(f"{BRIGHT_RED}>> ❌ El porcentaje debe ser un número entero mayor que cero y menor o igual a 100.{RESET}")
            else:
                print(f"{BRIGHT_RED}>> ❌ El número de observaciones no coincide con el tamaño de la muestra (n).{RESET}")
        else:
            print(f"{BRIGHT_RED}>> ❌ El formato de las observaciones no es correcto.{RESET}")
    else:
        print(f"{BRIGHT_RED}>> ❌ El tamaño de la muestra debe ser un número entero mayor o igual a 1.{RESET}")

def CocVarianzaPoblacional(RutaIMG10: str):
    """
    Para estimar un cociente de varianzas poblacionales.

    Esta función considera la única situación para estimar un cociente de varianzas poblacionales:

    - Para dos muestras independientes de poblaciones normales.

    Para ello se pide y se calculan los datos necesarios para obtener el intervalo de confianza. 

    Parameters
    ----------
    RutaIMG9 : str
        Ruta de la imagen de la fórmula del intervalo de confianza para la única situación.
    """
    TMuest1 = input("Escribe el tamaño de la muestra (n₁): ")
    if TMuest1.isdigit() and int(TMuest1) >= 1:
        Muest1 = input(f"\nEscribe las {TMuest1} observaciones (x₁ x₂ ... xₙ): ")
        if FormatoMuest(Muest1): # Se valida el formato de las observaciones
            if CantidadMuest(Muest1, TMuest1): # Se valida la cantidad de observaciones
                TMuest2 = input("\nEscribe el tamaño de la muestra (n₂): ")
                if TMuest2.isdigit() and int(TMuest2) >= 1:
                    Muest2 = input(f"\nEscribe las {TMuest2} observaciones (x₁ x₂ ... xₙ): ")
                    if FormatoMuest(Muest2): # Se valida el formato de las observaciones
                        if CantidadMuest(Muest2, TMuest2): # Se valida la cantidad de observaciones
                            PConf = input("\nEscribe el porcentaje (%) de confianza: ")
                            if PConf.isdigit() and 0 < int(PConf) <= 100:
                                # Mostrar mensajes de advertencia
                                if int(PConf) < 90:
                                    print(f"{BRIGHT_YELLOW}>> ⚠️ Usar un nivel de confianza menor a 90% implica un mayor riesgo de que el intervalo no contenga el valor real. Se recomienda 90% o más.{RESET}")
                                elif int(PConf) == 100:
                                    print(f"{BRIGHT_YELLOW}>> ⚠️ Un nivel de confianza del 100% genera un intervalo demasiado amplio y poco útil. Se recomienda usar 90%, 95% o 99%.{RESET}")

                                print(f"\n{BRIGHT_YELLOW}>> Los datos corresponden al caso 10{RESET}")
                                print(f"\n{BRIGHT_MAGENTA}- Parámetro a estimar: σ₁² / σ₂²{RESET}")
                                print(f"{BRIGHT_MAGENTA}- Situación: Para dos muestras independientes de poblaciones normales.{RESET}")
                                print(f"{BRIGHT_MAGENTA}- Estimador puntual: 𝑠₁² / 𝑠₂²{RESET}")

                                # Recuperamos los datos de la función
                                Intervalo, EstVar, RV, LitSup, LitInf, Gl1, Gl2 = ICCaso10(Muest1, Muest2, TMuest1, TMuest2, PConf)

                                # Se determina si las varianzas son iguales o diferentes, de acuerdo con el intervalo del cociente
                                match EstVar:
                                    case "SI":
                                        print(f"\n{BRIGHT_GREEN}>> ✅ El intervalo de confianza para el cociente de varianzas muestrales S₁² / S₂² = {RV} es: {Intervalo} y el 1 {EstVar} se encuentra en este{RESET}")
                                        GraficarIC_FC10(RV, LitSup, LitInf, Gl1, Gl2, f"Intervalo de confianza al {PConf}% para σ₁² / σ₂² (dos muestras independientes de poblaciones normales)\n n₁ = {TMuest1}, n₂ = {TMuest2}, S₁² / S₂² = {RV}", PConf, RutaIMG10)
                                    case "NO":
                                        print(f"\n{BRIGHT_GREEN}>> ✅ El intervalo de confianza para el cociente de varianzas muestrales S₁² / S₂² = {RV} es: {Intervalo} y el 1 {EstVar} se encuentra en este{RESET}")
                                        GraficarIC_FC10(RV, LitSup, LitInf, Gl1, Gl2, f"Intervalo de confianza al {PConf}% para σ₁² / σ₂² (dos muestras independientes de poblaciones normales)\n n₁ = {TMuest1}, n₂ = {TMuest2}, S₁² / S₂² = {RV}", PConf, RutaIMG10)
                            else:
                                print(f"{BRIGHT_RED}>> ❌ El porcentaje debe ser un número entero mayor que cero y menor o igual a 100.{RESET}")
                        else:
                            print(f"{BRIGHT_RED}>> ❌ El número de observaciones no coincide con el tamaño de la muestra (n₂).{RESET}")
                    else:
                        print(f"{BRIGHT_RED}>> ❌ El formato de las observaciones no es correcto.{RESET}")
                else:
                    print(f"{BRIGHT_RED}>> ❌ El tamaño de la muestra debe ser un número entero mayor o igual a 1.{RESET}")
            else:
                print(f"{BRIGHT_RED}>> ❌ El número de observaciones no coincide con el tamaño de la muestra (n₁).{RESET}")
        else:
            print(f"{BRIGHT_RED}>> ❌ El formato de las observaciones no es correcto.{RESET}")
    else:
        print(f"{BRIGHT_RED}>> ❌ El tamaño de la muestra debe ser un número entero mayor o igual a 1.{RESET}")