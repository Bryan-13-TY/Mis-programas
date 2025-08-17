"""
Calculadora de intervalos de confianza.

Archivo principal. Este archivo contiene el menú de la calculadora, en donde el usuario elije el parámetro que quiere estimar.

Autor: García Escamilla Bryan Alexis
Fecha: 16/08/2025
"""

from Casos import MediaPoblacional, DifMediaPoblacional, Proporcion, DifProporcion, VarianzaPoblacional, CocVarianzaPoblacional
import os # Para construir las rutas correctamente

BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_WHITE = "\033[97m"
RESET = "\033[0m"

print(f"""{BRIGHT_YELLOW}
/*---------------------------------------.
| CALCULADORA DE INTERVALOS DE CONFIANZA |      
`---------------------------------------*/{RESET}

>> Elige el parámetro a estimar
      
1.- Una media (μ)
2.- Una diferencia de medias (μ₁ - μ₂)
3.- Una proporción (𝑃)
4.- Una diferencia de proporciones (𝑃₁ - 𝑃₂)
5.- Una varianza poblacional (σ²)
6.- El cociente de varianzas poblacionales (σ₁² / σ₂²)
""")

Param = input("Opción: ")

match Param: # Determinar el párametro a estimar
    case '1':
        print(f"""{BRIGHT_YELLOW}
/*-------------------------------.
| Para una media poblacional (μ) |
`-------------------------------*/{RESET}

- Ingresa cada una de las muestras separadas por un espacio (x₁ x₂ ... xₙ) para calcular la media muestral (X̄).
- El tamaño de la muestra (n) debe coincidir con la cantidad de muestras ingresadas.
- (n) debe ser un número entero.
- Se recomienda que el porcentaje de confianza este entre 90% y 99%. Si este no se conoce usar 95%.
""")
        RutaIMG1 = os.path.join(os.path.dirname(__file__), "IMG", "CASO1.png")
        RutaIMG2 = os.path.join(os.path.dirname(__file__), "IMG", "CASO2.png")
        MediaPoblacional(RutaIMG1, RutaIMG2)
    case '2':
        print(f"""{BRIGHT_YELLOW}
/*------------------------------------------------------.
| Para una diferencia de medias poblacionales (μ₁ - μ₂) |              
`------------------------------------------------------*/{RESET}

- Ingresa cada una de las muestras separadas por un espacio (x₁ x₂ ... xₙ) para calcular las medias muestrales (X̄₁ y X̄₂) respectivamente.
- Los tamaños de las muestras (n₁ y n₂) deben coincidir con la cantidad de muestras ingresadas respectivamente.
- (n₁ y n₂) deben ser números enteros.
- Se recomienda que el porcentaje de confianza este entre 90% y 99%. Si este no se conoce usar 95%.
""")
        RutaIMG3 = os.path.join(os.path.dirname(__file__), "IMG", "CASO3.png")
        RutaIMG4 = os.path.join(os.path.dirname(__file__), "IMG", "CASO4.png")
        RutaIMG5 = os.path.join(os.path.dirname(__file__), "IMG", "CASO5.png")
        RutaIMG6 = os.path.join(os.path.dirname(__file__), "IMG", "CASO6.png")
        DifMediaPoblacional(RutaIMG3, RutaIMG4, RutaIMG5, RutaIMG6)
    case '3':
        print(f"""{BRIGHT_YELLOW}
/*------------------------.
| Para una proporción (𝑃) |
`------------------------*/{RESET}

- El número de éxitos (X) no debe ser mayor que el tamaño de la muestra (N).
- El tamaño de la muestra no debe ser menor que el número de éxitos.
- Tanto (X) como (N) deben ser números enteros.
- Se recomienda que el porcentaje de confianza este entre 90% y 99%. Si este no se conoce usar 95%.
""")
        RutaIMG7 = os.path.join(os.path.dirname(__file__), "IMG", "CASO7.png")
        Proporcion(RutaIMG7)
    case '4':
        print(f"""{BRIGHT_YELLOW}
/*----------------------------------------------.
| Para una diferencia de proporciones (𝑃₁ - 𝑃₂) |
`----------------------------------------------*/{RESET}
              
- El número de éxitos (X₁ y X₂) no deben ser mayores que los tamaños de la muestra (N₁ y N₂) respectivamente.
- Los tamaños de las muestras (N₁ y N₂) no deben ser menores que el número de éxitos (X₁ y X₂) respectivamente.
- Tanto (X₁ y X₂) como (N₁ y N₂) deben ser números enteros.
- Se recomienda que el porcentaje de confianza este entre 90% y 99%. Si este no se conoce usar 95%.
""")
        RutaIMG8 = os.path.join(os.path.dirname(__file__), "IMG", "CASO8.png")
        DifProporcion(RutaIMG8)
    case '5':
        print(f"""{BRIGHT_YELLOW}
/*-----------------------------------.
| Para una varianza poblacional (σ²) |
`-----------------------------------*/{RESET}
              
- Ingresa cada una de las muestras separadas por un espacio (x₁ x₂ ... xₙ) para calcular la media muestral (X̄).
- El tamaño de la muestra (n) debe coincidir con la cantidad de muestras ingresadas.
- (n) debe ser un número entero.
- Se recomienda que el porcentaje de confianza este entre 90% y 99%. Si este no se conoce usar 95%.
""")
        RutaIMG9 = os.path.join(os.path.dirname(__file__), "IMG", "CASO9.png")    
        VarianzaPoblacional(RutaIMG9)
    case '6':
        print(f"""{BRIGHT_YELLOW}
/*--------------------------------------------------------.
| Para el cociente de varianzas poblacionales (σ₁² / σ₂²) |
`--------------------------------------------------------*/{RESET}
              
- Ingresa cada una de las muestras separadas por un espacio (x₁ x₂ ... xₙ) para calcular las medias muestrales (X̄₁ y X̄₂) respectivamente.
- Los tamaños de las muestras (n₁ y n₂) deben coincidir con la cantidad de muestras ingresadas respectivamente.
- (n₁ y n₂) deben ser números enteros.
- Se recomienda que el porcentaje de confianza este entre 90% y 99%. Si este no se conoce usar 95%.
""")
        RutaIMG10 = os.path.join(os.path.dirname(__file__), "IMG", "CASO10.png")
        CocVarianzaPoblacional(RutaIMG10)
    case _: 
        print(f"{BRIGHT_RED}>> ERROR: {Param} No se encuentra entre las opciones.{RESET}")
