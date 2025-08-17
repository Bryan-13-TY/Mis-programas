"""
Calculos para los intervalos de confianza.

Esta archivo contiene las funciones para calcular todos los datos necesarios para los intervalos.

Autor: García Escamilla Bryan Alexis
Fecha: 16/08/2025
"""

import re # Necesario para usar expresiones regulares
import math # Necesario pata calcular raices
from scipy.stats import norm # Para calcular Z
from scipy.stats import t # Para calcular T
from scipy.stats import f # Para calcular F
from scipy.stats import chi2 # Para calcular Chi2

def FormatoMuest(Muest: str) -> bool:
    """
    Determina que el formato de una muestra sea válido.

    Esta función determina que el formato de una muestra sea válido usando una expresión regular.

    Parameters
    ----------
    Muest : str
        Muestra a validar.

    Returns
    -------
    bool
        True si el formato es válido, None en caso contrario.
    """
    # Expresión regular para las muestras
    Formato = r'^\d+(\.\d+)?( \d+(\.\d+)?)*$'

    # Regresa un valor booleano
    return re.fullmatch(Formato, Muest.strip()) is not None

def CantidadMuest(Muest: str, TMuest: str) -> bool:
    """
    Verifica que el número de observaciones de una muestra corresponda con el tamaño de la muestra.

    Parameters
    ----------

    Muest : str
        Muestra a verificar con el formato correcto.
    TMuest : str
        Tamaño de la muestra.
    
    Returns
    -------
    bool
        True si coincide, False en caso contrario.
    """
    LMuest = (Muest.strip()).split(" ")

    if len(LMuest) == int(TMuest):
        return True
    else:
        return False

def FloatInt(Dato: str) -> bool:
    """
    Verifica si el dato es un número decimal o entero.

    Parameters
    ----------
    Dato : str
        Dato de entrada a verificar.

    Returns
    -------
    bool
        True si es un número decimal o entero, False en caso contrario.
    """
    try:
        Numero = float(Dato)
        if Numero.is_integer():
            return True
        else:
            return True
    except ValueError:
        return False

def CalcularMedia(Muest: str) -> float:
    """
    Calcula la media de una muestra.

    Esta función separa la muestra quitando los espacios y guardando los números en una lista. Esta es reccorida y los números se convierten de cadena a flotantes.
    Al final estos números se guardan en otra lista a parte para después ser sumados.

    Parameters
    ----------
    Muest : str
        Muestra a sumar con el formato correcto.
    
    Returns
    -------
    float
        Media de la muestra.
    """
    # Separar los números
    Numeros = (Muest.strip()).split(" ")

    # Convertir los números a flotantes
    NumerosFloat = []
    for Numero in Numeros:
        NumerosFloat.append(float(Numero))

    # Se regresa la media calculada
    return round(sum(NumerosFloat) / len(NumerosFloat), 4)

def CalcularS2(TMuest: str, Muest: str, Media: float) -> float:
    """
    Calcula el valor de S^2.

    Esta función calcula el valor de S^2, necesario para algunos intervalos.

    Parameters
    ----------
    TMuest : str
        Tamaño de la muestra.
    Muest : str
        Muestra necesaria con el formato correcto.
    Media : float
        Media de la muestra.
    
    Returns
    -------
    float
        Valor de S^2 con cuatro decimales.
    """
    # Separar los números
    Numeros = (Muest.strip()).split(" ")
    Suma = 0 

    # Hacemos la suma
    for Muestra in range(int(TMuest)):
        Suma = round(Suma + ((float(Numeros[Muestra]) - Media) ** 2), 4)

    # Se calcula el valor de S2
    S2 = (1 / (int(TMuest) - 1)) * Suma

    # Regresa el valor de S2
    return round(S2, 4)

def CalcularV(S12: float, S22: float, TMuest1: str, TMuest2: str) -> float:
    """
    Calcula el valor de v.

    Esta función calcula el valor de v para los grados de libertad para algunos intervalos.

    Parameters
    ----------
    S12 : float
        Valor de S^2_1.
    S22 : float
        Valor de S^2_2.
    TMuest1 : str
        Tamaño de la primera muestra.
    TMuest2 : str
        Tamaño de la segunda muestra.
    
    Returns
    -------
    float
        Valor de v con cuatro decimales.
    """
    # Se calcula el valor de V
    Numerador = ((S12 / int(TMuest1)) + (S22 / int(TMuest2))) ** 2
    Denominador = (((S12 / int(TMuest1)) ** 2) / (int(TMuest1) + 1)) + (((S22 / int(TMuest2)) ** 2) / (int(TMuest2) + 1))
    V = (Numerador / Denominador) - 2

    # Regresa el valor de v
    return round(V, 4)

def CalcularSp(S12: float, S22: float, TMuest1: str, TMuest2: str) -> float:
    """
    Calcula el valor de S_p.

    Esta función calcula el valor de S_p para algunos intervalos.

    Parameters
    ----------
    S12 : float
        Valor de S^2_1.
    S22 : float
        Valor de S^2_2.
    TMuest1 : str
        Tamaño de la primera muestra.
    TMuest2 : str
        Tamaño de la segunda muestra.
    
    Returns
    -------
    float
        Valor de V_p con cuatro decimales.
    """
    # Se calcula el valor de Vp
    Vp = math.sqrt((((int(TMuest1) - 1) * S12) + ((int(TMuest2) - 1) * S22)) / (int(TMuest1) + int(TMuest2) - 2))

    # Regresa el valor de Vp
    return round(Vp, 4)

def Calcularp(NoExit: str, TMuest: str) -> float:
    """
    Calcula el valor de 𝑝.

    Esta función calcula el valor de 𝑝 para algunos intervalos.

    Parameters
    ----------
    NoExit : str
        Números de éxitos de la muestra.
    TMuest : str
        Tamaño de la muestra.

    Returns
    -------
    float
        Valor de 𝑝 con cuatro decimales.
    """
    # Se calcula el valor de 𝑝
    p = int(NoExit) / int(TMuest)

    # Regresa el valor de p
    return round(p, 4)

def CalcularZAlpha2(PConf: str) -> float:
    """
    Calcula el valor crítico de la distribución Z (normal).

    Parameters
    ----------
    PConf : str
        Porcentaje de confianza.
    
    Returns
    -------
    float
        Valor de Z con cuatro decimales.
    """
    # Se calcula el valor de alpha
    Alpha = 1 - float(int(PConf) / 100)

    # Se calcula el valor de Z
    Z = norm.ppf(1 - round(Alpha / 2, 4))

    # Regresa el valor de Z
    return round(Z, 4)

def CalcularTAlpha2(PConf: str, GL: str | float, Caso: int) -> float:
    """
    Calcula el valor crítico de la distribución T (t de Student).

    Esta función calcula el valor crítico de la distribución T para tres casos diferentes.

    Parameters
    ----------
    PConf : str
        Porcentaje de confianza.
    GL : str | float
        Grados de libertad de la distribución.
    Caso : int
        Caso en donde se requiere calcular los grados de libertar de una distribución T.
    
    Returns
    -------
    float
        Valor crítico de la distribución T con tres decimales.
    """
    # Se calcula el valor de alpha
    Alpha = 1 - float(int(PConf) / 100)

    # Se determina el número de caso para calcular el valor crítico correspondiente
    if (Caso == 2):
        # Se calculan los grados de libertad
        Gl = int(GL) - 1 

        # Se calcula el valor de T
        T = t.ppf(1 - round(Alpha / 2, 4), Gl)
    elif (Caso == 5):
        Gl = GL

        # Se calcula el valor de T
        T = t.ppf(1 - round(Alpha / 2, 4), Gl)
    else: # Caso 6
        Gl = GL - 2

        # Se calcula el valor de T
        T = t.ppf(1 - round(Alpha / 2, 4), Gl)

    # Regresa el valor de T
    return round(T, 3)

def CalcularFAlpha2(PConf: str, TMuest1: str, TMuest2: str) -> tuple[float, float]:
    """
    Calcula los dos valores críticos de la distribución F de Fisher.

    Esta función calcula el valor crítico de la distribución F para el intervalo superior e inferior.

    Parameters
    ----------
    PConf : str
        Porcentaje de confianza.
    TMuest1 : str
        Tamaño de la primera muestra.
    TMuest2 : str
        Tamaño de la segunda muestra.

    Returns
    -------
        tuple
            (F superior, F inferior)
        
            - **F superior** (float): valor crítico de la distribución F del intervalo superior con tres decimales.
            - **F inferior** (float): valor crítico de la distribución F del intervalo inferior con tres decimaless.
    """
    # Se calcula el valor de alpha
    Alpha = 1 - float(int(PConf) / 100)

    # Se calculan los grados de libertad
    Gl1 = int(TMuest2) - 1
    Gl2 = int(TMuest1) - 1

    # Se calcula el valor de F Superior
    FSup = f.ppf(1 - (Alpha / 2), Gl1, Gl2) 

    # Se calcula el valor de F Inferior
    FInf = f.ppf(Alpha / 2, Gl1, Gl2)

    # Regresa el valor de FSup y FInf
    return round(FSup, 3), round(FInf, 3)

def CalcularChiAlpha2(PConf: str, TMuest: str) -> tuple[float, float]:
    """
    Calcula los dos valores críticos de la de la distribución Chi cuadrada (X^2).

    Esta dfunción calcula el valor crítico de la distribución Chi cuadrada para el intervalo superior e inferior.

    Parameters
    ---------
    PConf : str
        Porcentaje de confianza.
    TMuest : str
        Tamaño de la muestra.
    
    Returns
    -------
    tuple
        (Chi inferior, Chi superior)

        - **Chi inferior** (float): valor crítico de la distribución Chi cuadrada del intervalo inferior con tres decimales.
        - **Chi superior** (float): valor crítico de la distribución Chi cuadrada del intervalo superior con tres decimales. 
    """
    # Se calcula el valor de alpha
    Alpha = 1 - float(int(PConf) / 100)

    # Se calculan los grados de libertad
    Gl = int(TMuest) - 1

    # Se calcula el valor de Chi2 superior
    Chi2Sup = chi2.ppf(1 - (Alpha / 2), Gl)

    # Se calcula el valor de Chi2 inferior
    Chi2Inf = chi2.ppf(Alpha / 2, Gl)

    # Regresa el valor de Chi2Sup, Chi2Inf
    return round(Chi2Sup, 3), round(Chi2Inf, 3)

def ICCaso1(Muest: str, TMuest: str, DesEstPob: float, PConf: str) -> tuple[str, float, float, float]:
    """
    Calcula el intervalo de confianza para la situación 1:

    - Distribución normal, muestra grande y varianza conocida.
    - Distribución normal, muestra grande y varianza desconocida.

    Parameters
    ----------
    Muest : str
        Muestra con el formato correcto.
    TMuest : str
        Tamato de la muestra.
    DesEstPob : float
        Desviación estándar poblacional.
    PConf : str
        Porcentaje de confianza.
    
    Returns
    -------
    tuple
        (Invertavalo, Media, Limite superior, Limite inferior)

        - **Intervalo** (str): intervalo de confianza para la situación 1 con dos decimales.
        - **Media** (float): media de la muestra con dos decimales.
        - **Limite superior** (float): limite supeior del intervalo.
        - **Limite inferior** (float): limite inferior del intervalo.
    """
    # Obtenemos algunos datos
    MediaZ = CalcularMedia(Muest)
    Z = CalcularZAlpha2(PConf)

    # Se calculan ambos intervalos
    IntervaloL = MediaZ - (Z * (DesEstPob / math.sqrt(int(TMuest))))
    IntervaloU = MediaZ + (Z * (DesEstPob / math.sqrt(int(TMuest))))

    # Se regresa el IC
    return f"[{round(IntervaloL, 2)}, {round(IntervaloU, 2)}]", round(MediaZ, 2), IntervaloU, IntervaloL

def ICCaso2(Muest: str, TMuest: str, PConf: str) -> tuple[str, float, float, float, float]:
    """
    Calcula el intervalo de confianza para la situación 2:

    - Distribución normal, muestra grande y varianza desconocida.
    - Distribución normal, muestra pequeña y varianza desconocida.

    Parameters
    ----------
    Muest : str
        Muestra con el formato correcto.
    TMuest : str
        Tamaño de la muestra.
    PConf : str
        Porcentaje de confianza.

    Returns
    -------
    tuple
        (Intervalo, Media, Limite superior, Limite inferior, S)

        - **Intervalo** (str): intervalo de confianza para la situación 2 con dos decimales.
        - **Media** (float): media de la muestra con dos decimales.
        - **Limite superior** (float): limite superior del intervalo.
        - **Limite inferior** (float): limite inferior del intervalo.
        - **S** (float): valor de S.
    """
    # Obtenemos algunos datos
    MediaT = CalcularMedia(Muest)
    T = CalcularTAlpha2(PConf, TMuest, 2)
    S = math.sqrt(CalcularS2(TMuest, Muest, MediaT))

    # Se calculan ambos intervalos
    IntervaloL = MediaT - (T * (S / math.sqrt(int(TMuest))))
    IntervaloU = MediaT + (T * (S / math.sqrt(int(TMuest))))

    return f"[{round(IntervaloL, 2)}, {round(IntervaloU, 2)}]", round(MediaT, 2), IntervaloU, IntervaloL, S

def ICCaso3(Muest1: str, Muest2: str, DesEstPob1: float, DesEstPob2: float, TMuest1: str, TMuest2: str, PConf: str) -> tuple[str, float, float, float]:
    """
    Calcula el intervalo de confianza para la situación 3:

    - Para dos muestras independientes de poblaciones normales con varianzas conocidas.

    Parameters
    ----------
    Muest1 : str
        Primera muestra con el formato correcto.
    Muest2 : str
        Segunda muestra con el formato correcto.
    DesEstPob1 : float
        Primera desviación estándar poblacional.
    DesEstPob2 : float
        Segunda desviación estándar poblacional.
    TMuest1 : str
        Tamaño de la primera muestra.
    TMuest2 : str
        Tamaño de la segunda muestra.
    PConf : str
        Porcentaje de confianza.

    Returns
    -------
    tuple
        (Intervalo, Diferencia de medias, Limite superior, Limite inferior)

        - **Intervalo** (str): intervalo de confianza para la situación 3 con dos decimales.
        - **Diferencia de medias** (float): diferencia entre dos medias con dos decimales.
        - **Limite superior** (float): limite superior del intervalo.
        - **Limite inferior** (float): limite inferior del intervalo.
    """
    # Obtenemos algunos datos
    MediaZ1 = CalcularMedia(Muest1)
    MediaZ2 = CalcularMedia(Muest2)
    Z = CalcularZAlpha2(PConf)

    # Se calculan ambos intervalos
    IntervaloL = (MediaZ1 - MediaZ2) - (Z * math.sqrt(((DesEstPob1 ** 2) / int(TMuest1)) + ((DesEstPob2 ** 2) / int(TMuest2))))
    IntervaloU = (MediaZ1 - MediaZ2) + (Z * math.sqrt(((DesEstPob1 ** 2) / int(TMuest1)) + ((DesEstPob2 ** 2) / int(TMuest2))))

    # Se regresa el IC
    return f"[{round(IntervaloL, 2)}, {round(IntervaloU, 2)}]", round(MediaZ1 - MediaZ2, 2), IntervaloU, IntervaloL

def ICCaso4(Muest1: str, Muest2: str, TMuest1: str, TMuest2: str, PConf: str) -> tuple[str, float, float, float, float]:
    """
    Calcula el intervalo de confianza para la situación 4:
    
    - Para dos muestras grandes (n > 30) independientes de poblaciones normales con varianzas diferentes y desconocidas.

    Parameter
    ---------
    Muest1 : str
        Primera muestra con el formato correcto.
    Muest2 : str
        Segunda muestra con el formato correcto.
    TMuest1 : str
        Tamaño de la primera muestra.
    TMuest2 : str
        Tamaño de la segunda muestra.
    PConf : str
        Porcentaje de confianza.
    
    Returns
    -------
    tuple
        (Intervalo, Diferencia de medias, Limite superior, Limite inferior, Z)

        - **Intervalo** (str): intervalo de confianza para la situación 4 con dos decimales.
        - **Diferencia de medias** (float): diferencia entre dos medias con dos decimales.
        - **Limite superior** (float): limite superior del intervalo.
        - **Limite inferior** (float): limite inferior del intervalo.
        - **Z** (float): valor crítico de la distribución Z.
    """
    # Obtenemos algunos datos
    MediaZ1 = CalcularMedia(Muest1)
    MediaZ2 = CalcularMedia(Muest2)
    Z = CalcularZAlpha2(PConf)
    S12 = CalcularS2(TMuest1, Muest1, MediaZ1)
    S22 = CalcularS2(TMuest2, Muest2, MediaZ2)

    # Se calculan ambos intervalos
    IntervaloL = (MediaZ1 - MediaZ2) - (Z * math.sqrt((S12 / int(TMuest1)) + (S22 / int(TMuest2))))
    IntervaloU = (MediaZ1 - MediaZ2) + (Z * math.sqrt((S12 / int(TMuest1)) + (S22 / int(TMuest2))))
    
    # Se regresa el IC
    return f"[{round(IntervaloL, 2)}, {round(IntervaloU, 2)}]", round(MediaZ1 - MediaZ2, 2), IntervaloU, IntervaloL, Z

def ICCaso5(Muest1: str, Muest2: str, TMuest1: str, TMuest2: str, PConf: str) -> tuple[str, float, float, float, float, float]:
    """
    Calcula el intervalo de confianza para la situación 5:

    - Para dos muestras chicas independientes de poblaciones normales con varianzas diferentes y desconocidas.

    Parameters
    ----------
    Muest1 : str
        Primera muestra con el formato correcto.
    Muest2 : str
        Segunda muestra con el formato correcto.
    TMuest1 : str
        Tamaño de la primera muestra.
    TMuest2 : str
        Tamaño de la segunda muestra.
    PConf : str
        Porcentaje de confianza.

    Returns
    -------
    tuple
        (Intervalo, Diferencia de medias, Limite superior, Limite inferior, T, Gl)

        - **Intervalo** (str): intervalo de confianza para la situación 5 con dos decimales.
        - **Diferencia de medias** (float): diferencia entre dos medias con dos decimales.
        - **Limite superior** (float): limite superior del intervalo.
        - **Limite inferior** (float): limite inferior del intervalo.
        - **T** (float): valor crítico de la distribución T.
        - **Gl** (float): grados de libertad de la distribución T.
    """
    # Obtenemos algunos datos
    MediaT1 = CalcularMedia(Muest1)
    MediaT2 = CalcularMedia(Muest2)
    S12 = CalcularS2(TMuest1, Muest1, MediaT1)
    S22 = CalcularS2(TMuest2, Muest2, MediaT2)
    V = CalcularV(S12, S22, TMuest1, TMuest2)
    T = CalcularTAlpha2(PConf, V, 5)

    # Se calculan ambos intervalos
    IntervaloL = (MediaT1 - MediaT2) - (T * math.sqrt((S12 / int(TMuest1)) + (S22 / int(TMuest2))))
    IntervaloU = (MediaT1 - MediaT2) + (T * math.sqrt((S12 / int(TMuest1)) + (S22 / int(TMuest2))))

    # Se regresa el IC
    return f"[{round(IntervaloL, 2)}, {round(IntervaloU, 2)}]", round(MediaT1 - MediaT2, 2), IntervaloU, IntervaloL, T, V

def ICCaso6(Muest1: str, Muest2: str, TMuest1: str, TMuest2: str, PConf: str) -> tuple[str, float, float, float, float, float]:
    """
    Calcula el intervalo de confianza para la situación 6:

    - Para dos muestras independientes de poblaciones normales con varianzas iguales y desconocidas.

    Parameters
    ----------
    Muest1 : str
        Primera muestra con el formato correcto.
    Muest2 : str
        Segunda muestra con el formato correcto.
    TMuest1 : str
        Tamaño de la primera muestra.
    TMuest2 : str
        Tamaño de la segunda muestra.
    PConf : str
        Porcentaje de confianza.

    Returns
    -------
    tuple
        (Intervalo, Diferencia de medias, Limite superior, Limite inferior, T, Gl)

        - **Intervalo** (str): intervalo de confianza para la situación 5 con dos decimales.
        - **Diferencia de medias** (float): diferencia entre dos medias con dos decimales.
        - **Limite superior** (float): limite superior del intervalo.
        - **Limite inferior** (float): limite inferior del intervalo.
        - **T** (float): valor crítico de la distribución T.
        - **Gl** (float): grados de libertad de la distribución T con dos decimales.
    """
    # Obtenemos algunos datos
    MediaT1 = CalcularMedia(Muest1)
    MediaT2 = CalcularMedia(Muest2)
    S12 = CalcularS2(TMuest1, Muest1, MediaT1)
    S22 = CalcularS2(TMuest2, Muest2, MediaT2)
    Sp = CalcularSp(S12, S22, TMuest1, TMuest2)
    T = CalcularTAlpha2(PConf, float(int(TMuest1) + int(TMuest2)), 6)

    # Se calculan ambos intervalos
    IntervaloL = (MediaT1 - MediaT2) - (T * Sp * math.sqrt((1 / int(TMuest1)) + (1 / int(TMuest2))))
    IntervaloU = (MediaT1 - MediaT2) + (T * Sp * math.sqrt((1 / int(TMuest1)) + (1 / int(TMuest2))))

    # Se regresa el IC
    return f"[{round(IntervaloL, 2)}, {round(IntervaloU, 2)}]", round(MediaT1 - MediaT2, 2), IntervaloU, IntervaloL, T, round(int(TMuest1 + TMuest2) - 2, 2)

def ICCaso7(NoExit: str, TMuest: str, PConf: str) -> tuple[str, float, float, float, float]:
    """
    Calcula el intervalo de confianza para la situación 7:
    
    - Para una muestra grande con 𝑃 pequeña.

    Parameters
    ----------
    NoExit : str
        Número de éxitos de la muestra.
    TMuest : str
        Tamaño de la muestra.
    PConf : str
        Porcentaje de confianza.

    Returns
    -------
    tuple
        (Intervalo, p, Limite superior, Limite inferior, Z)

        - **Intervalo** (str): intervalo de confianza para la situación 7 con dos decimales.
        - **p** (float): Proporción.
        - **Limite superior** (float): limite superior del intervalo.
        - **Limite inferior** (float): limite inferior del intervalo.
        - **Z** (float): valor crítico de la distribución Z.
    """
    # Obtenemos algunos datos
    p = Calcularp(NoExit, TMuest)
    Z = CalcularZAlpha2(PConf)

    # Se calculan ambos intervalos
    IntervaloL = p - (Z * math.sqrt((p * (1 - p)) / int(TMuest)))
    IntervaloU = p + (Z * math.sqrt((p * (1 - p)) / int(TMuest)))

    # Se regresa el IC
    return f"[{round(IntervaloL, 2)}, {round(IntervaloU, 2)}]", p, IntervaloU, IntervaloL, Z

def ICCaso8(NoExit1: str, NoExit2: str, TMuest1: str, TMuest2: str, PConf: str) -> tuple[str, float, float, float, float]:
    """
    Calcula el intervalo de confianza para la situación 8:

    - Para dos muestras grandes e independientes de una distribución normal.

    Parameters
    ----------
    NoExist1 : str
        Número de éxitos de la primera muestra.
    NoExist2 : str
        Número de éxitos de la segunda muestra.
    TMuest1 : str
        Tamaño de la primera muestra.
    TMuest2 : str
        Tamaño de la segunda muestra.
    PConf : str
        Porcentaje de confianza.
    
    Returns
    -------
    tuple
        (Intervalo, Diferencia de proporciones, Limite superior, Limite Inferior, Z)

        - **Intervalor** (str): intervalo de confianza para la situación 8 con dos decimales.
        - **Diferencia de proporciones** (float): diferencia entre dos proporciones con dos decimales.
        - **Limite superior** (float): limite superior del intervalo.
        - **Limite inferior** (float): limite inferior del intervalo.
        - **Z** (float): valor crítico de la distribución Z.
    """
    # Obtenemos algunos datos
    p1 = Calcularp(NoExit1, TMuest1)
    p2 = Calcularp(NoExit2, TMuest2)
    Z = CalcularZAlpha2(PConf)

    # Se calculan ambos intervalos
    IntervaloL = (p1 - p2) - (Z * math.sqrt(((p1 * (1 - p1)) / int(TMuest1)) + ((p2 * (1 - p2)) / int(TMuest2))))
    IntervaloU = (p1 - p2) + (Z * math.sqrt(((p1 * (1 - p1)) / int(TMuest1)) + ((p2 * (1 - p2)) / int(TMuest2))))

    # Se regresa el IC
    return f"[{round(IntervaloL, 2)}, {round(IntervaloU, 2)}]", round(p1 - p2, 2), IntervaloU, IntervaloL, Z

def ICCaso9(Muest: str, TMuest: str, PConf: str) -> tuple[str, float, float, float, float]:
    """
    Calcula el intervalo de confianza para la situación 9:

    - Para una muestra cualquiera.

    Parameters
    ----------
    Muest : str
        Muestra con el formato correcto.
    TMuest : str
        Tamaño de la muestra.
    PConf : str
        Porcentaje de confianza.

    Returns
    -------
    tuple
        (Intervalo, S, Limite superior, Limite inferior, Gl)

        - **Intervalo** (str): intervalo de confianza para la situación 9 con dos decimales.
        - **S** (float): valor de S.
        - **Limite superior** (float): limite superior del intervalo.
        - **Limite inferior** (float): limite inferior del intervalo.
        - **Gl** (float): grados de libertad para la distribución Chi cuadrada.
    """
    # Obtenemos algunos datos
    MediaX = CalcularMedia(Muest)
    S2 = CalcularS2(TMuest, Muest, MediaX)
    Chi2Sup, Chi2Inf = CalcularChiAlpha2(PConf, TMuest)

    # Se calculan ambos intervalos
    IntervaloL = (S2 * (int(TMuest) - 1)) / Chi2Sup
    IntervaloU = (S2 * (int(TMuest) - 1)) / Chi2Inf

    # Se regresa el IC
    return f"[{round(IntervaloL, 2)}, {round(IntervaloU, 2)}]", S2, IntervaloU, IntervaloL, float(TMuest) - 1

def ICCaso10(Muest1: str, Muest2: str, TMuest1: str, TMuest2: str, PConf: str) -> tuple[str, str, float, float, float, float, float]:
    """
    Calcula el intervalo de confianza para la situación 10:
    
    - Para dos muestras independientes de poblaciones normales.

    Parameters
    ----------
    Muest1 : str
        Primera muestra con el formato correcto.
    Muest2 : str
        Segunda muestra con el formato correcto.
    TMuest1 : str
        Tamaño de la primera muestra.
    TMuest2 : str
        Tamaño de la segunda muestra.
    PConf : str
        Porcentaje de confianza.

    Returns
    -------
    tuple
        (Intervalo, Estatus, CVM, Limite superior, Limite inferior, Grados de libertad 1, Grados de libertad 2)

        - **Intervalo** (str): intervalo de confianza para la situación 10 con dos decimales.
        - **Estaus** (str): SI, si el uno están en el intervalo, NO en caso contrario.
        - **CVM** (float): cociente de varianza muestrales, con dos decimales.
        - **Limite superior** (float): limite superior del intervalo.
        - **Limite inferior** (float): limite inferior del intervalo.
        - **Grados de libertad 1** (float): grados de libertad 1.
        - **Grados de libertad 2** (float): grados de libertad 1.
    """
    # Obtenemos algunos datos
    MediaF1 = CalcularMedia(Muest1)
    MediaF2 = CalcularMedia(Muest2)
    S12 = CalcularS2(TMuest1, Muest1, MediaF1)
    S22 = CalcularS2(TMuest2, Muest2, MediaF2)
    FSup, FInf = CalcularFAlpha2(PConf, TMuest1, TMuest2)

    # Se calculan amnbos intervalos
    IntervaloL = (S12 / S22) * (1 / FSup)
    IntervaloU = (S12 / S22) * (1 / FInf)

    # Se determina si las varianzas son iguales o diferentes
    if (IntervaloL <= 1 <= IntervaloU):
        EstatusV = "SI"
    else: 
        EstatusV = "NO"

    # Se regresa el IC
    return f"[{round(IntervaloL, 2)}, {round(IntervaloU, 2)}]", EstatusV, round(S12 / S22, 2), IntervaloU, IntervaloL, float(TMuest1) - 1, float(TMuest2) - 1