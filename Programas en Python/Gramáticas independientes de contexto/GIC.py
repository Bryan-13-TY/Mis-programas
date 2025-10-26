"""
Gramática independiente de contexto.

Autor: García Escamilla Bryan Alexis

Fecha: 26/10/2025

Descripción:
    Este archivo evalúa una expresión numérica en C, usando gramáticas independientes de contexto.
"""

import nltk, os, msvcrt
from nltk import CFG
from automatas import automata_pila, automata_constantes_numericas, automata_variables

# Alfabetos
hex = ['A','B','C','D','E','F']

variables = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o'
             ,'p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E'
             ,'F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T'
             ,'U','V','W','X','Y','Z','_','$']

signos_invalidos = [',','{','}','[',']','','"',"'",'|','°','¬','^'
                    ,'¨','?','¡','¿','$','#','.','~','´']

reservadas = ['auto','break','case','char','const','continue','default','do','double','else'
              ,'enum','extern','float','for','goto','if','inline','int','long','register'
              ,'restrict','return','short','signed','sizeof','static','struct','switch','typedef','union'
              ,'unsigned','void','volatile','while','_Alignas','_Alignof','_Atomic','_Bool','_Complex','Decimal128'
              ,'_Decimal32','_Decimal64','_Generic','_Imaginary','_Noreturn','_Static_assert','_Thread_local']

reservadas_tipo = ['char','short','int','long','float','double','asigned','unsigned'
                   ,'_Bool','_Complex','_Decimal32','_Decimal64','_Decimal128']

# Códigos de color ANSI

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
ORANGE = "\033[33m"
RESET = "\033[0m"

def limpiar_terminal() -> None:
    """
    Limpia la terminal de cualquier sistema operativo. 
    """
    os.system('cls' if os .name == 'nt' else 'clear')

def esperar_tecla():
    """
    Espera a que se presione cualquier tecla.
    """
    return msvcrt.getch().decode("utf-8")  # devuelve la tecla como string

def separar_tokens(expresion: str) -> list[str]:
    """
    Separa la expresión por tokens.

    Parameters
    ----------
    expresion : str
        Expresión ingresada por el usuario.

    Returns
    -------
    list[str]
        Lista con los tokens de la expresión.
    """
    tokens = []
    buffer = ""

    for caracter in expresion:
        if (caracter.isdigit() or caracter.isalpha()): # Si es un número o una letra
            buffer = buffer + caracter # Se acumula
        elif (caracter == " "):
            continue # Se ignoran los espacios en blanco
        else: # Si es un operador o un paréntesis
            if (buffer != ""): # Si hay un número o variable en construcción
                tokens.append(buffer)
                buffer = ""
                tokens.append(caracter)
            else:
                tokens.append(caracter)

    return tokens

def arbol_derivacion(expresion_gramatica: str) -> None:
    """
    Muestra el árbol de derivación de la expresión si cumple con la gramática.

    Parameters
    ----------
    expresion_gramatica : str
        Expresion a evaluar por la gramática.
    """
    # Se define la gramática
    gramatica = CFG.fromstring("""
    S -> E ';'
    E -> 'v' '=' A | 'v' '=' R | R '+' T | R '-' T | T '*' F | T '/' F | T '%' F | 'v' | 'c' | '(' R ')'
    A -> 'v' '=' A | 'v' '=' R
    R -> R '+' T | R '-' T | T '*' F | T '/' F | T '%' F | 'v' | 'c' | '(' R ')'
    T -> T '*' F | T '/' F | T '%' F | 'v' | 'c' | '(' R ')'
    F -> 'v' | 'c' | '(' R ')'
    """)

    # Crear el parser y el árbol de derivación
    paser = nltk.ChartParser(gramatica)

    # Intenta parsear y mostrar los árboles de derivación
    try:
        found_parse = False

        for tree in paser.parse(expresion_gramatica.split()):
            found_parse = True

            print("\nElige como quiere que se muestre el árbol de derivación: 1 = Modo Texto, 2 = Modo Gráfico, 3 = Ambos Modos\n")

            opcion = input("Opción: ")

            match (opcion):
                case '1':
                    print("\nÁrbol de derivación:\n")

                    tree.pretty_print()
                case '2':
                    print("\nÁrbol de derivación:\n")

                    tree.pretty_print()
                case '3':
                    print("\nÁrbol de derivación:\n")

                    tree.pretty_print()
                    tree.draw()
                case _:
                    print("\nOpción no válida")
            
            if (not found_parse):
                print("\nNo se encontraron árboles de derivación válidos")
    except ValueError as error:
        print(f"\nNo se puede analizar la expresión: {error}")

def filtro_1(tokens: list[str], hex: list[str]) -> tuple[str, str, int]:
    """
    Clasifica los tokens de la expresión.

    Parameters
    ----------
    tokens : list[str]
        Lista con la expresión separada por tokens.
    hex : list[str]
        Lista con los números en hexadecimal.

    Returns
    -------
    tuple
        (expresion_automata, expresion_gramatica, key)
        
        - **expresion_automata** (str): expresión a evaluar por el automata de pila.
        - **expresion_gramatica** (str): expresión a evaluar por la gramática.
        - **key** (int): llave para abrir o cerrar el filtro 2.
    """
    # Se clasifica cada token de la expresión

    # Constante Numérica = C
    # Cosntante Numérica Incorrecta = M
    # Variable = V
    # Variable Incorrecta = W
    # Palabra Reservada = P
    # Operadores = O
    # Signo de Asignación = A
    # Paréntesis de Apertura = Y
    # Paréntesis de Cierre = Z
    # Palabra Reservada para Constantes Numéricas = H
    # Punto y coma = X

    expresion_automata = "" # Expresión a evaluar a mandar a validar por el autómata
    expresion_gramatica = "" # Expresión e evaluar a mandar a validar por la gramática
    key = 0 # Llave para pasar de filtro 1 al filtro 2

    for token in tokens:
        if (token.isalpha() and token in reservadas): # Si es una palabra reservada
            if (token in reservadas_tipo): # Si es una palabra reservada con valor númerico
                expresion_automata = expresion_automata + 'H'
                expresion_gramatica = expresion_gramatica + 'h' + " "
            else: # Si es una palabra reservada sin valor numérico
                expresion_automata = expresion_automata + 'P'
                expresion_gramatica = expresion_gramatica + 'p' + " "
        else: # Si no es una palabra reservada
            if (token.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-'))): # Si es un número
                if (automata_constantes_numericas(token, hex)): # Si es una constante numérica
                    expresion_automata = expresion_automata + 'C'
                    expresion_gramatica = expresion_gramatica + 'c' + " "
                else: # Si no es una constante numérica
                    if (token == '+' or token == '-'): # Si es un operador
                        expresion_automata = expresion_automata + 'O'
                        expresion_gramatica = expresion_gramatica + token + " "
                    else: # Si es una constante numérica incorrecta
                        expresion_automata = expresion_automata + 'M'
                        expresion_gramatica = expresion_gramatica + 'm' + " "

                        key = 1 # Filtro 2 cerrado
            else: # Si no es un número
                if (automata_variables(token, variables)): # Si es una variable
                    expresion_automata = expresion_automata + 'V'
                    expresion_gramatica = expresion_gramatica + 'v' + " "
                else: # Si no es una variable
                    if (token == '/' or token == '*' or token == '%'): # Si es un operador
                        expresion_automata = expresion_automata + 'O'
                        expresion_gramatica = expresion_gramatica + token + " "
                    elif (token == '='): # Si es una asignación
                        expresion_automata = expresion_automata + 'A'
                        expresion_gramatica = expresion_gramatica + token + " "
                    elif (token == '('): # Si es un paréntesis de apertura
                        expresion_automata = expresion_automata + 'Y'
                        expresion_gramatica = expresion_gramatica + token + " "
                    elif (token == ')'): # Si es un paréntesis de cierre
                        expresion_automata = expresion_automata + 'Z'
                        expresion_gramatica = expresion_gramatica + token + " "
                    elif (token == ';'): # Si la expresión termino
                        expresion_automata = expresion_automata + 'X'
                        expresion_gramatica = expresion_gramatica + token
                    else: # Si es una variable incorrecta
                        if (token in signos_invalidos):
                            key = 1 # Filtro 2 cerrado
                        else:
                            if (not automata_variables(token, variables)): # Si es una variable incorrecta
                                expresion_automata = expresion_automata + 'W'
                                expresion_gramatica = expresion_gramatica + 'w' + " "
                                key = 1 # Filtro 2 cerrado

    return expresion_automata, expresion_gramatica, key

def filtro_2(key: int, expresion: str, expresion_automata: str, expresion_gramatica: str) -> None:
    """
    Evalua la expresión por medio del autómata de pila.

    Parameters
    ----------
    key : int
        Llave para abrir o cerrar el filtro 2.
    expresion : str
        Expresion ingresada por el usuario.
    expresion_automata : str
        Expresion a evaluar por el autómata de pila.
    expresion_gramatica : str
        Expresión a evaluar por la gramática.
    """
    if (key == 0): # El segundo filtro se abre
        # Se valida el autómata de pila
        mensaje, state, _, pila_2 = automata_pila(expresion, expresion_automata, state='q0', pila_1=['z0'], pila_2=['z0'])

        if (mensaje != ""):
            print(f"\n{mensaje}")
        else:
            if (state == 'q4' and not pila_2):
                print(f"\n{GREEN}La expresión{RESET} {YELLOW}{expresion}{RESET} {GREEN}pertenece a la gramática (Por F2){RESET}")
                arbol_derivacion(expresion_gramatica)
            elif (state != 'q4' and pila_2):
                print(f"\n{RED}La expresión{RESET} {YELLOW}{expresion}{RESET} {RED}no pertenece a la gramática (Por F2){RESET}")
            elif (state != 'q4' or pila_2):
                print(f"\n{RED}La expresión{RESET} {YELLOW}{expresion}{RESET} {RED}no pertenece a la gramática (Por F2){RESET}")
    else:
        print(f"{RED}La expresión{RESET} {YELLOW}{expresion}{RESET} {RED}no pertenece a la gramática (Por F1){RESET}")

def main() -> None:
    while (True):
        limpiar_terminal()
        print("""
/*--------------------------------------.
| GRAMÁTICAS INDEPENDIENTES DE CONTEXTO |              
`--------------------------------------*/

>> Elije una opción
              
1.- Evaluar una expresión en C
2.- Salir del programa
""")
        opcion = input("Opción: ").strip()

        match(opcion):
            case '1':
                expresion = input("\nIngresa una expresión: ").strip()
                tokens = separar_tokens(expresion) # Tokens de la expresión

                print(f"\nTokens de la expresión: {tokens}")

                expresion_automata, expresion_gramatica, key = filtro_1(tokens, hex)
    
    
                print(f"\nLa expresión a validar por el autómata es: {expresion_automata}")
                print(f"La expresión a validar por la gramática es: {expresion_gramatica}\n")

                filtro_2(key, expresion, expresion_automata, expresion_gramatica)

                # Esperamos una tecla
                print("\n>> Presiona una tecla para continuar...")
                tecla = esperar_tecla()
            case '2':
                print("\n>> Gracias por probar el programa, vuelva pronto")

                break
            case _:
                print("\n>> La opción no es válida")

if __name__ == "__main__":
    main()