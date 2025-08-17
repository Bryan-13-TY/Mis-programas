"""
Gráficas de los intervalos de confianza.

Este archivo contiene las funciones para graficar el intervao de confianza de cada situación.

Autor: García Escamilla Bryan Alexis
Fecha: 17/08/2025
"""

import matplotlib.pyplot as plt # Para graficar los intervalos de confianza
import matplotlib.image as mpimg # Para agregar una imagen al gráfico
import numpy as np
from scipy.stats import norm # Para calcular Z
from scipy.stats import t # Para calcular T
from scipy.stats import f # Para calcular F
from scipy.stats import chi2 # Para calcular Chi2

def GraficarIC_ZC1(Media: float, LitSup: float, LitInf: float, DEstand: float, n: float, Titulo: str, PConf: str, RutaIMG: str):
    """
    Grafica el intervalo de confianza para la situación 1:

    - Distribución normal, muestra grande y varianza conocida.
    - Distribución normal, muestra grande y varianza desconocida.

    Parameters
    ----------

    Media : float
        Media de la muestra.
    LitSup : float
        Limite superior del intervalo.
    LitInf : float
        Limite inferior del intervalo.
    DEstand : float
        Desviación estándar.
    n : float
        Tamaño de la muestra.
    Titulo : str
        Título de la gráfica.
    PConf : str
        Porcentaje de confianza.
    RutaIMG : str
        Ruta de la imagen de la fórmula del intervalo de confianza.
    """
    # Calcular error estándar
    se = DEstand / np.sqrt(n)

    # Rango para la distribución normal
    x = np.linspace(Media - 4 * se, Media + 4 * se, 1000)
    y = norm.pdf(x, loc=Media, scale=se)

    # Intentar cargar la imagen
    try:
        imagen = mpimg.imread(RutaIMG)
    except FileNotFoundError:
        print(f"⚠️ Imagen no encontrada en la ruta: {RutaIMG}")
        return

    # Crear figura con 2 subplots (gráfica + imagen)
    fig, axs = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [3, 1]})

    # Parte 1: Gráfica
    axs[0].plot(x, y, label='Distribución Z (normal)', color='black')

    # Sombrear solo el nivel de confianza
    axs[0].fill_between(x, y, where=(x >= LitInf) & (x <= LitSup), color='green', alpha=0.3, label=f"Nivel de confianza = {PConf}%")

    # Líneas verticales
    axs[0].axvline(LitInf, color='red', linestyle='--', label=f"Límite inferior = {LitInf:.2f}")
    axs[0].axvline(LitSup, color='red', linestyle='--', label=f"Límite superior = {LitSup:.2f}")
    axs[0].axvline(Media, color='blue', linestyle='--', label=f"Media (X̄) = {Media:.2f}")

    # Título y etiquetas
    axs[0].set_title(Titulo)
    axs[0].set_xlabel("Valor de μ")
    axs[0].set_ylabel("Densidad de probabilidad")
    axs[0].legend(loc='upper left')
    axs[0].grid(True)

    # Parte 2: Imagen
    axs[1].imshow(imagen)
    axs[1].axis('off')  # Oculta ejes

    plt.tight_layout()
    plt.show()

def GraficarIC_TC2(Media: float, LitSup: float, LitInf: float, S: float, n: float, Titulo: str, PConf: str, RutaIMG: str):
    """
    Grafica el intervalo de confianza para la situación 2:

    - Distribución normal, muestra grande y varianza desconocida.
    - Distribución normal, muestra pequeña y varianza desconocida.

    Parameters
    ----------
    Media : float
        Media de la muestra.
    LitSup : float
        Limite superior del intervalo.
    LitInf : float
        Limite inferior del intervalo.
    S : float
        Valor de S.
    n : float
        Tamaño de la muestra.
    Titulo : str
        Título de la gráfica.
    PConf : str
        Porcentaje de confianza.
    RutaIMG : str
        Ruta de la imagen de la fórmula del intervalo de confianza.
    """
    # Calcular el error estándar
    se = S / np.sqrt(n)

    # Crear dominio para la curva t centrada en Media
    x = np.linspace(Media - 4*se, Media + 4*se, 1000)
    # Distribución t centrada en media y escalada (ya que usamos t_alpha2 externo, aquí solo graficamos pdf t estándar centrada en Media)
    y = np.power((1 + ((x - Media)/se)**2 / (n-1)), -(n)/2)  # t pdf formula alternativa
    # Mejor usar scipy.stats.t.pdf con df=n-1 para exactitud:
    from scipy.stats import t
    y = t.pdf((x - Media)/se, df=n-1) / se

    # Intentar cargar la imagen
    try:
        imagen = mpimg.imread(RutaIMG)
    except FileNotFoundError:
        print(f"⚠️ Imagen no encontrada en la ruta: {RutaIMG}")
        return
    
    # Crear figura con 2 subplots (gráfica + imagen)
    fig, axs = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [3, 1]})

    # Parte 1: Gráfica
    axs[0].plot(x, y, label='Distribución t (t de Student)', color='black')

    # Sombrear solo el Nivel de confianza
    axs[0].fill_between(x, y, where=(x >= LitInf) & (x <= LitSup), color='green', alpha=0.3, label=f"Nivel de confianza = {PConf}%")

    # Líneas verticales
    axs[0].axvline(LitInf, color='red', linestyle='--', label=f"Límite inferior = {LitInf:.2f}")
    axs[0].axvline(LitSup, color='red', linestyle='--', label=f"Límite superior = {LitSup:.2f}")
    axs[0].axvline(Media, color='blue', linestyle='--', label=f"Media (X̄) = {Media:.2f}")

    # Título y etiquetas
    axs[0].set_title(Titulo)
    axs[0].set_xlabel("Valor de (μ)")
    axs[0].set_ylabel("Densidad de probabilidad")
    axs[0].legend(loc='upper left')
    axs[0].grid(True)
    
    # Parte 2: Imagen
    axs[1].imshow(imagen)
    axs[1].axis('off') # Oculta ejes

    plt.tight_layout()
    plt.show()

def GraficarIC_ZC3(DifMedia: float, LitSup: float, LitInf: float, Titulo: str, PConf: str, RutaIMG: str):
    """
    Grafica el intervalo de confianza para la situación 3:

    - Para dos muestras independientes de poblaciones normales con varianzas conocidas.

    Parameters
    ----------
    DifMedia : float
        Diferencia entre las dos medias.
    LitSup : float
        Limite superior del intervalo.
    LitInf : float
        Limite inferior del intervalo.
    Titulo : str
        Título de la gráfica.
    PConf : str
        Porcentaje de confianza.
    RutaIMG : str
        Ruta de la imagen de la fórmula del intervalo de confianza.
    """
    # Aproximar error estándar desde los límites si se quiere la curva
    se_aprox = (LitSup - LitInf) / 2  # Z * se ≈ margen → margen = IC_sup - DifMedia = Z·se
    x = np.linspace(DifMedia - 4*se_aprox, DifMedia + 4*se_aprox, 1000)
    y = norm.pdf(x, loc=DifMedia, scale=se_aprox)

    # Intentar cargar la imagen
    try:
        imagen = mpimg.imread(RutaIMG)
    except FileNotFoundError:
        print(f"⚠️ Imagen no encontrada en la ruta: {RutaIMG}")
        return
    
    # Crear figura con 2 subplots (gráfica + imagen)
    fig, axs = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [3, 1]})

    # Parte 1: Gráfica
    axs[0].plot(x, y, color='black', label='Distribución Z (normal)')

    # Sombrear solo el Nivel de confianza
    axs[0].fill_between(x, y, where=(x >= LitInf) & (x <= LitSup), color='green', alpha=0.3, label=f"Nivel de confianza = {PConf}%")

    # Líneas verticales
    axs[0].axvline(LitInf, color='red', linestyle='--', label=f"Límite inferior = {LitInf:.2f}")
    axs[0].axvline(LitSup, color='red', linestyle='--', label=f"Límite superior = {LitSup:.2f}")
    axs[0].axvline(DifMedia, color='blue', linestyle='--', label=f"Diferencia de medias (X̄₁ - X̄₂) = {DifMedia:.2f}")

    # Título y etiquetas
    axs[0].set_title(Titulo)
    axs[0].set_xlabel("Valor de (μ₁ - μ₂)")
    axs[0].set_ylabel("Densidad de probabilidad")
    axs[0].legend(loc='upper left')
    axs[0].grid(True)

    # Parte 2: Imagen
    axs[1].imshow(imagen)
    axs[1].axis('off') # Oculta ejes

    plt.tight_layout()
    plt.show()

def GraficarIC_ZC4(DifMedia: float, LitSup: float, LitInf: float, Z: float, Titulo: str, PConf: str, RutaIMG: str):
    """
    Grafica el intervalo de confianza para la situación 4:

    - Para dos muestras grandes (n > 30) independientes de poblaciones normales con varianzas diferentes y desconocidas.

    Parameters
    ----------
    DifMedia : float
        Diferencia entra las dos medias.
    LitSup : float
        Limite superior del intervalo.
    LitInf : float
        Limite inferior del intervalo.
    Z : float
        Valor crítico de la distribución Z.
    Titulo : str
        Título de la gráfica.
    PConf : str
        Porcentaje de confianza.
    RutaIMG : str
        Ruta de la imagen de la fórmula del intervalo de confianza.
    """
    # Estimar error estándar inversamente a partir del margen (opcional)
    se_aprox = (LitSup - LitInf) / (2 * Z)

    # Rango para la curva
    x = np.linspace(DifMedia - 4 * se_aprox, DifMedia + 4 * se_aprox, 1000)
    y = norm.pdf(x, loc=DifMedia, scale=se_aprox)

    # Intentar cargar la imagen
    try:
        imagen = mpimg.imread(RutaIMG)
    except FileNotFoundError:
        print(f"⚠️ Imagen no encontrada en la ruta: {RutaIMG}")
        return
    
    # Crear figura con 2 subplots (gráfica + imagen)
    fig, axs = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [3, 1]})

    # Parte 1: Gráfica
    axs[0].plot(x, y, label='Distribución Z (normal)', color='black')

    # Sombrear solo el Nivel de confianza
    axs[0].fill_between(x, y, where=(x >= LitInf) & (x <= LitSup), color='green', alpha=0.3, label=f"Nivel de confianza = {PConf}%")

    # Líneas verticales
    axs[0].axvline(LitInf, color='red', linestyle='--', label=f"Límite inferior = {LitInf:.2f}")
    axs[0].axvline(LitSup, color='red', linestyle='--', label=f"Límite superior = {LitSup:.2f}")
    axs[0].axvline(DifMedia, color='blue', linestyle='--', label=f"Diferencia de medias (X̄₁ - X̄₂) = {DifMedia:.2f}")

    # Título y etiquetas
    axs[0].set_title(f"{Titulo}")
    axs[0].set_xlabel("Valor de la diferencia (μ₁ - μ₂)")
    axs[0].set_ylabel("Densidad de probabilidad")
    axs[0].legend(loc='upper left')
    axs[0].grid(True)

    # Parte 2: Imagen
    axs[1].imshow(imagen)
    axs[1].axis('off') # Oculta ejes

    plt.tight_layout()
    plt.show()

def GraficarIC_TC5(DifMedia: float, LitSup: float, LitInf: float, T: float, Gl: float, Titulo: str, PConf: str, RutaIMG: str):
    """
    Grafica el intervalo de confianza para la situación 5:

    - Para dos muestras chicas independientes de poblaciones normales con varianzas diferentes y desconocidas.

    Parameters
    ----------
    DifMedia : float
        Diferencia entra las dos medias.
    LitSup : float
        Limite superior del intervalo.
    LitInf : float
        Limite inferior del intervalo.
    T : float
        Valor crítico de la distribución T.
    Gl : float
        Grados de libertad.
    Titulo : str
        Título de la gráfica.
    PConf : str
        Porcentaje de confianza.
    RutaIMG : str
        Ruta de la imagen de la fórmula del intervalo de confianza.
    """
    # Estimar error estándar desde el margen (opcional, solo para graficar)
    se_aprox = (LitSup - LitInf) / (2 * T)

    # Dominio para curva t
    x = np.linspace(DifMedia - 4 * se_aprox, DifMedia + 4 * se_aprox, 1000)
    y = t.pdf((x - DifMedia) / se_aprox, df=Gl) / se_aprox  # Escalada

    # Intentar cargar la imagen
    try:
        imagen = mpimg.imread(RutaIMG)
    except FileNotFoundError:
        print(f"⚠️ Imagen no encontrada en la ruta: {RutaIMG}")
        return

    # Crear figura con 2 subplots (gráfica + imagen)
    fig, axs = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [3, 1]})

    # Parte 1: Gráfica
    axs[0].plot(x, y, color='black', label='Distribución t (t de Welch)')

    # Sombrear solo el Nivel de confianza
    axs[0].fill_between(x, y, where=(x >= LitInf) & (x <= LitSup), color='green', alpha=0.3, label=f"Nivel de confianza = {PConf}%")

    # Líneas verticales
    axs[0].axvline(LitInf, color='red', linestyle='--', label=f"Límite inferior = {LitInf:.2f}")
    axs[0].axvline(LitSup, color='red', linestyle='--', label=f"Límite superior = {LitSup:.2f}")
    axs[0].axvline(DifMedia, color='blue', linestyle='--', label=f"Diferencia de medias (X̄₁ - X̄₂) = {DifMedia:.2f}")

    # Título y etiquetas
    axs[0].set_title(Titulo)
    axs[0].set_xlabel("Valor de la diferencia (μ₁ - μ₂)")
    axs[0].set_ylabel("Densidad de probabilidad")
    axs[0].legend(loc='upper left')
    axs[0].grid(True)

    # Parte 2: Imagen
    axs[1].imshow(imagen)
    axs[1].axis('off') # Oculta ejes

    plt.tight_layout()
    plt.show()

def GraficarIC_TC6(DifMedia: float, LitSup: float, LitInf: float, T: float, Gl: float, Titulo: str, PConf: str, RutaIMG: str):
    """
    Grafica el intervalo de confianza para la situación 6:

    - Para dos muestras independientes de poblaciones normales con varianzas iguales y desconocidas.

    Parameters
    ----------
    DifMedia : float
        Diferencia entra las dos medias.
    LitSup : float
        Limite superior del intervalo.
    LitInf : float
        Limite inferior del intervalo.
    T : float
        Valor crítico de la distribución T.
    Gl : float
        Grados de libertad.
    Titulo : str
        Título de la gráfica.
    PConf : str
        Porcentaje de confianza.
    RutaIMG : str
        Ruta de la imagen de la fórmula del intervalo de confianza.
    """
    # Aproximación del error estándar a partir del margen (solo para la curva)
    se_aprox = (LitSup - LitInf) / (2 * T)

    # Dominio para la curva t
    x = np.linspace(DifMedia - 4 * se_aprox, DifMedia + 4 * se_aprox, 1000)
    y = t.pdf((x - DifMedia) / se_aprox, df=Gl) / se_aprox

    # Intentar cargar la imagen
    try:
        imagen = mpimg.imread(RutaIMG)
    except FileNotFoundError:
        print(f"⚠️ Imagen no encontrada en la ruta: {RutaIMG}")
        return    

    # Crear figura con 2 subplots (gráfica + imagen)
    fig, axs = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [3, 1]})

    # Parte 1: Gráfica
    axs[0].plot(x, y, color='black', label='Distribución t (t de Student)')

    # Sombrear solo el Nivel de confianza
    axs[0].fill_between(x, y, where=(x >= LitInf) & (x <= LitSup), color='green', alpha=0.3, label=f"Nivel de confianza = {PConf}%")

    # Líneas
    axs[0].axvline(LitInf, color='red', linestyle='--', label=f"Límite inferior = {LitInf:.2f}")
    axs[0].axvline(LitSup, color='red', linestyle='--', label=f"Límite superior = {LitSup:.2f}")
    axs[0].axvline(DifMedia, color='blue', linestyle='--', label=f"Diferencia de medias (X̄₁ - X̄₂) = {DifMedia:.2f}")

    # Estética
    axs[0].set_title(Titulo)
    axs[0].set_xlabel("Valor de la diferencia (μ₁ - μ₂)")
    axs[0].set_ylabel("Densidad de probabilidad")
    axs[0].legend(loc='upper left')
    axs[0].grid(True)

    # Parte 2: Imagen
    axs[1].imshow(imagen)
    axs[1].axis('off') # Oculta ejes

    plt.tight_layout()
    plt.show()

def GraficarIC_ZC7(p: float, LitSup: float, LitInf: float, Z: float, Titulo: str, PConf: str, RutaIMG: str):
    """
    Grafica el intervalo de confianza para la situación 7:

    - Para una muestra grande con 𝑃 pequeña.

    Parameters
    ----------
    p : float
        Proporción.
    LitSup : float
        Limite superior del intervalo.
    LitInf : float
        Limite inferior del intervalo.
    Z : float
        Valor crítico de la distribución Z.
    Titulo : str
        Título de la gráfica.
    PConf : str
        Porcentaje de confianza.
    RutaIMG : str
        Ruta de la imagen de la fórmula del intervalo de confianza.
    """
    # Estimar error estándar inverso desde los márgenes (solo para graficar)
    se_aprox = (LitSup - LitInf) / (2 * Z)

    # Rango para la curva
    x = np.linspace(p - 4 * se_aprox, p + 4 * se_aprox, 1000)
    y = norm.pdf(x, loc=p, scale=se_aprox)

    # Intentar cargar la imagen
    try:
        imagen = mpimg.imread(RutaIMG)
    except FileNotFoundError:
        print(f"⚠️ Imagen no encontrada en la ruta: {RutaIMG}")
        return
    
    # Crear figura con 2 subplots (gráfica + imagen)
    fig, axs = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [3, 1]})

    # Parte 1: Gráfica
    axs[0].plot(x, y, color='black', label='Distribución Normal (Z)')

    # Sombrear solo el Nivel de confianza
    axs[0].fill_between(x, y, where=(x >= LitInf) & (x <= LitSup), color='green', alpha=0.3, label=f"Nivel de confianza = {PConf}%")

    # Líneas verticales
    axs[0].axvline(LitInf, color='red', linestyle='--', label=f"Límite inferior = {LitInf:.3f}")
    axs[0].axvline(LitSup, color='red', linestyle='--', label=f"Límite superior = {LitSup:.3f}")
    axs[0].axvline(p, color='blue', linestyle='--', label=f"Proporción muestral p = {p:.3f}")

    # Título y etiquetas
    axs[0].set_title(Titulo)
    axs[0].set_xlabel("Valor de la proporción (p)")
    axs[0].set_ylabel("Densidad de probabilidad")
    axs[0].legend(loc='upper left')
    axs[0].grid(True)

    # Parte 2: Imagen
    axs[1].imshow(imagen)
    axs[1].axis('off') # Oculta ejes

    plt.tight_layout()
    plt.show()

def GraficarIC_ZC8(Dp: float, LitSup: float, LitInf: float, Z: float, Titulo: str, PConf: str, RutaIMG: str):
    """
    Grafica el intervalo de confianza para la situación 8:

    - Para dos muestras grandes e independientes de una distribución normal.

    Parameters
    ----------
    Dp : float
        Diferencia entre las proporciones.
    LitSup : float
        Limite superior del intervalo.
    LitInf : float
        Limite inferior del intervalo.
    Z : float
        Valor crítico de la distribución Z.
    Titulo : str
        Título de la gráfica.
    PConf : str
        Porcentaje de confianza.
    RutaIMG : str
        Ruta de la imagen de la fórmula del intervalo de confianza.
    """
    # Estimar error estándar desde el margen (solo para graficar)
    se_aprox = (LitSup - LitInf) / (2 * Z)

    # Rango para la curva normal
    x = np.linspace(Dp - 4 * se_aprox, Dp + 4 * se_aprox, 1000)
    y = norm.pdf(x, loc=Dp, scale=se_aprox)

    # Intentar cargar la imagen
    try:
        imagen = mpimg.imread(RutaIMG)
    except FileNotFoundError:
        print(f"⚠️ Imagen no encontrada en la ruta: {RutaIMG}")
        return
    
    # Crear figura con 2 subplots (gráfica + imagen)
    fig, axs = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [3, 1]})

    # Parte 1: Gráfica
    axs[0].plot(x, y, color='black', label='Distribución Z (normal)')

    # Sombrear solo el Nivel de confianza
    axs[0].fill_between(x, y, where=(x >= LitInf) & (x <= LitSup), color='green', alpha=0.3, label=f"Nivel de confianza = {PConf}%")

    # Líneas verticales
    axs[0].axvline(LitInf, color='red', linestyle='--', label=f"Límite inferior = {LitInf:.3f}")
    axs[0].axvline(LitSup, color='red', linestyle='--', label=f"Límite superior = {LitSup:.3f}")
    axs[0].axvline(Dp, color='blue', linestyle='--', label=f"Diferencia de proporciones (p₁ - p₂) = {Dp:.3f}")
    
    # Título y etiquetas
    axs[0].set_title(Titulo)
    axs[0].set_xlabel("Valor de la diferencia (P₁ - P₂)")
    axs[0].set_ylabel("Densidad de probabilidad")
    axs[0].legend(loc='upper left')
    axs[0].grid(True)

    # Parte 2: Imagen
    axs[1].imshow(imagen)
    axs[1].axis('off') # Oculta ejes

    plt.tight_layout()
    plt.show()

def GraficarIC_XC9(S2: float, LitSup: float, LitInf: float, Gl: float, Titulo: str, PConf: str, RutaIMG: str):
    """
    Grafica el intervalo de confianza para la situación 9:

    - Para una muestra cualquiera.

    Parameters
    ----------
    S2 : float
        Valor de S^2.
    LitSup : float
        Limite superior del intervalo.
    LitInf : float
        Limite inferior del intervalo.
    Gl : float
        Grados de libertad.
    Titulo : str
        Título de la gráfica.
    PConf : str
        Porcentaje de confianza.
    RutaIMG : str
        Ruta de la imagen de la fórmula del intervalo de confianza.
    """
    # Rango para valores de sigma²
    x = np.linspace(0.01, LitSup * 1.5, 1000)
    chi_vals = (Gl * S2) / x  # Cambio de variable: x = (gl * s²) / χ²
    y = chi2.pdf(chi_vals, df=Gl) * (Gl * S2) / (x**2)  # PDF transformada

    # Intentar cargar la imagen
    try:
        imagen = mpimg.imread(RutaIMG)
    except FileNotFoundError:
        print(f"⚠️ Imagen no encontrada en la ruta: {RutaIMG}")
        return
    
    # Crear figura con 2 subplots (gráfica + imagen)
    fig, axs = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [3, 1]})

    # Parte 1: Gráfica
    axs[0].plot(x, y, label='Distribución X² (Chi-cuadrada)', color='black')

    # Sombrear solo el Nivel de confianza
    axs[0].fill_between(x, y, where=(x >= LitInf) & (x <= LitSup), color='green', alpha=0.3, label=f"Nivel de confianza = {PConf}%")
    
    # Líneas verticales
    axs[0].axvline(LitInf, color='red', linestyle='--', label=f"Límite inferior = {LitInf:.2f}")
    axs[0].axvline(LitSup, color='red', linestyle='--', label=f"Límite superior = {LitSup:.2f}")
    axs[0].axvline(S2, color='blue', linestyle='--', label=f"Varianza muestral (S²) = {S2:.2f}")

    # Estética
    axs[0].set_title(Titulo)
    axs[0].set_xlabel("Valor de la varianza (σ²)")
    axs[0].set_ylabel("Densidad de probabilidad")
    axs[0].legend(loc='upper right')
    axs[0].grid(True)

    # Parte 2: Imagen
    axs[1].imshow(imagen)
    axs[1].axis('off') # Oculta ejes

    plt.tight_layout()
    plt.show()

def GraficarIC_FC10(RV: float, LitSup: float, LitInf: float, Gl1: float, Gl2: float, Titulo: str, PConf: str, RutaIMG: str):
    """
    Grafica el intervalo de confianza para la situación 10:

    - Para dos muestras independientes de poblaciones normales.

    Parameters
    ----------
    RV : float
        Cociente de varianzas muestrales.
    LitSup : float
        Limite superior del intervalo.
    LitInf : float
        Limite inferior del intervalo.
    Gl1 : float
        Grados de libertad 1.
    Gl2 : float
        Grados de libertad 2.
    Titulo : str
        Título de la gráfica.
    PConf : str
        Porcentaje de confianza.
    RutaIMG : str
        Ruta de la imagen de la fórmula del intervalo de confianza.
    """
    # Dominio para la curva de la razón
    x = np.linspace(0.01, LitSup * 1.5, 1000)
    f_vals = (x / RV)
    y = f.pdf(f_vals, dfn=Gl1, dfd=Gl2) / RV  # Transformación del PDF de F

    # Intentar cargar la imagen
    try:
        imagen = mpimg.imread(RutaIMG)
    except FileNotFoundError:
        print(f"⚠️ Imagen no encontrada en la ruta: {RutaIMG}")
        return
    
    # Crear figura con 2 subplots (gráfica + imagen)
    fig, axs = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [3, 1]})

    # Parte 1: Gráfica
    axs[0].plot(x, y, color='black', label='Distribución F (F de Fisher)')

    # Sombrear solo el Nivel de confianza
    axs[0].fill_between(x, y, where=(x >= LitInf) & (x <= LitSup), color='green', alpha=0.3, label=f"Nivel de confianza = {PConf}%")

    # Líneas verticales
    axs[0].axvline(LitInf, color='red', linestyle='--', label=f"Límite inferior = {LitInf:.3f}")
    axs[0].axvline(LitSup, color='red', linestyle='--', label=f"Límite superior = {LitSup:.3f}")
    axs[0].axvline(RV, color='blue', linestyle='--', label=f"Razón muestral (S₁² / S₂²) = {RV:.3f}")

    # Estética
    axs[0].set_title(Titulo)
    axs[0].set_xlabel("Razón de varianzas (σ₁² / σ₂²)")
    axs[0].set_ylabel("Densidad de probabilidad")
    axs[0].legend(loc='upper right')
    axs[0].grid(True)

    # Parte 2: Imagen
    axs[1].imshow(imagen)
    axs[1].axis('off') # Oculta ejes

    plt.tight_layout()
    plt.show()