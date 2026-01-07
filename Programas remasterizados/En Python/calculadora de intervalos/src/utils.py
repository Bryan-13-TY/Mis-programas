"""
Docstring for Programas remasterizados.En Python.calculadora de intervalos.src.utils

Contiene constantes y funciones útiles para el programa.

Author: García Escamilla Bryan Alexis
Date: 07/01/2026
Version: 1.0
"""

import os
import msvcrt

BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_WHITE = "\033[97m"
RESET = "\033[0m"

def clear_console() -> None:
    os.system('cls' if os .name == 'nt' else 'clear')


def wait_key() -> None:
    msvcrt.getch()


def show_info(text: str) -> None:
    """
    Docstring for show_info

    Muestra texto con información, espera a que se presione enter y
    borra la consola.
    
    :param text: Texto con la información a mostrar.
    :type text: str
    """
    print(text)
    wait_key()
    clear_console()