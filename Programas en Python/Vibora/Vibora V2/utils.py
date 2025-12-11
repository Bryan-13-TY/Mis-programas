import random

negro = (0 ,0, 0)
verde = (0, 255, 0)
rojo = (255, 0, 0)
blanco = (255, 255, 255)

def color():
    colores = {"rojo": (228, 3, 3),
               "naranja": (255, 140, 0),
               "amarillo": (255, 237, 0),
               "verde": (0, 128, 38),
                "azul": (0, 77, 255),
                "violeta": (117, 7, 135)}

    colores_list = list(colores.values())
    color = colores_list[random.randrange(0, len(colores_list))]

    return color