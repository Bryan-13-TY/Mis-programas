"""
Docstring for Programas remasterizados.En Python.calculadora de intervalos.main

Menú de la calculadora donde se elije el parámetro a estimar.

Author: García Escamilla Bryan Alexis
Date: 06/01/2026
Version: 1.0
"""

from src.utils import (
    clear_console,
    wait_key,
    show_info,
)

from config.config import (
    MENU_PRINCIPAL,
    INFO_MEDIA_POBLACIONAL,
    INFO_DIF_MEDIA_POBLACIONALES,
    INFO_PROPORCION,
    INFO_DIF_PROPORCIONES,
    INFO_VARIANZA_POBLACIONAL,
    INFO_COC_VARIANZAS_POBLACIONALES,
    TEXT_NO_VALIDO,
)

def main() -> None:
    clear_console()

    while True:
        print(MENU_PRINCIPAL)
        
        param = input("Opción: ").strip().lower()
        match param:
            case "1":
                show_info(INFO_MEDIA_POBLACIONAL)
            case "2":
                show_info(INFO_DIF_MEDIA_POBLACIONALES)
            case "3":
                show_info(INFO_PROPORCION)
            case "4":
                show_info(INFO_DIF_PROPORCIONES)
            case "5":
                show_info(INFO_VARIANZA_POBLACIONAL)
            case "6":
                show_info(INFO_COC_VARIANZAS_POBLACIONALES)
            case "salir":
                break
            case _:
                print(TEXT_NO_VALIDO)
                wait_key()
                clear_console()

if __name__ == "__main__":
    main()