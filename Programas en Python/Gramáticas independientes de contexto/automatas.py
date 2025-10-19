"""
Autómatas para evaluación de la expresión en C.

Autor: García Escamilla Bryan Alexis

Fecha: 18/10/2025

Descripción:
    Este archivo contiene los autómatas necesarios para la evaluación de la expresión en C.
"""

from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State

# Códigos de color ANSI

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
ORANGE = "\033[33m"
RESET = "\033[0m"

def automata_pila(expresion: str, expresion_automata: str, state: str, pila_1: list[str], pila_2: list[str]) -> tuple[str, str, list[str], list[str]]:
    """
    Autómata de pila para evaluar la expresión.

    Parameters
    ----------
    expresion : str
        Expresión ingresada por el usuario.
    expresion_automata : str
        Expresión a evaluar por el autómata.
    state : str
        Estado actual en el autómata.
    pila_1 : list[str]
        Pila para los tokens de la expresión.
    pila_2 : list[str]
        Pila para los paréntesis de la expresión.

    Returns
    -------
    tuple
        (mensaje, state, pila_1, pila_2)

        - **mensaje** (str): mensaje después del autómata.
        - **state** (str): estado final después del autámata.
        - **pila_1** (list[str]): pila de los tokens después del autómata.
        - **pila_2** (list[str]): pila de los paréntesis después del autómata. 
    """
    print("Proceso de validación de la expresión:\n")

    for letra in expresion_automata:
        match (state):
            case 'q0':
                if (letra == 'V' and pila_1[-1] == 'z0'):
                    pila_1.append(letra)
                    state = 'q1'

                    print(f"Transicion 1: Caracter: {GREEN}{letra}{RESET}, Pila1: {YELLOW}{pila_1}{RESET}, Pila2: {MAGENTA}{pila_2}{RESET} Estado: {CYAN}{state}{RESET}")
                else:
                    return f"{RED}La expresión{RESET} {YELLOW}{expresion}{RESET} {RED}no pertenece a la gramática (Por F2){RESET}", state, pila_1, pila_2
            case 'q1':
                if (letra == 'A' and pila_1[-1] == 'V'):
                    pila_1.append(letra)
                    state = 'q2'

                    print(f"Transicion 2: Caracter: {GREEN}{letra}{RESET}, Pila1: {YELLOW}{pila_1}{RESET}, Pila2: {MAGENTA}{pila_2}{RESET} Estado: {CYAN}{state}{RESET}")        
            case 'q2':
                if (letra == 'V' and pila_1[-1] == 'A'):
                    pila_1.append(letra)
                    state = 'q2'
                    
                    print(f"Transicion 3: Caracter: {GREEN}{letra}{RESET}, Pila1: {YELLOW}{pila_1}{RESET}, Pila2: {MAGENTA}{pila_2}{RESET} Estado: {CYAN}{state}{RESET}")
                elif (letra == 'C' and pila_1[-1] == 'A'):
                    pila_1.append(letra)
                    state = 'q2'
                    
                    print(f"Transicion 4: Caracter: {GREEN}{letra}{RESET}, Pila1: {YELLOW}{pila_1}{RESET}, Pila2: {MAGENTA}{pila_2}{RESET} Estado: {CYAN}{state}{RESET}")
                elif (letra == 'Y' and pila_2[-1] == 'z0'):
                    pila_2.append('Pa')
                    state = 'q2'

                    print(f"Transicion 5: Caracter: {GREEN}{letra}{RESET}, Pila1: {YELLOW}{pila_1}{RESET}, Pila2: {MAGENTA}{pila_2}{RESET} Estado: {CYAN}{state}{RESET}")
                elif (letra == 'Z' and pila_2[-1] == 'Pa'):
                    del pila_2[-1]
                    state = 'q2'

                    print(f"Transicion 6: Caracter: {GREEN}{letra}{RESET}, Pila1: {YELLOW}{pila_1}{RESET}, Pila2: {MAGENTA}{pila_2}{RESET} Estado: {CYAN}{state}{RESET}")
                elif (letra == 'Y' and pila_2[-1] == 'Pa'):
                    pila_2.append('Pa')
                    state = 'q2'
                    
                    print(f"Transicion 7: Caracter: {GREEN}{letra}{RESET}, Pila1: {YELLOW}{pila_1}{RESET}, Pila2: {MAGENTA}{pila_2}{RESET} Estado: {CYAN}{state}{RESET}")
                elif (letra == 'A' and pila_1[-1] == 'V'):
                    pila_1.append(letra)
                    state = 'q2'
                    
                    print(f"Transicion 8: Caracter: {GREEN}{letra}{RESET}, Pila1: {YELLOW}{pila_1}{RESET}, Pila2: {MAGENTA}{pila_2}{RESET} Estado: {CYAN}{state}{RESET}")
                elif (letra == 'O' and pila_1[-1] == 'V'):
                    pila_1.append(letra)
                    state = 'q3'
                    
                    print(f"Transicion 9: Caracter: {GREEN}{letra}{RESET}, Pila1: {YELLOW}{pila_1}{RESET}, Pila2: {MAGENTA}{pila_2}{RESET} Estado: {CYAN}{state}{RESET}")
                elif (letra == 'O' and pila_1[-1] == 'C'):
                    pila_1.append(letra)
                    state = 'q3'
                    
                    print(f"Transicion 10: Caracter: {GREEN}{letra}{RESET}, Pila1: {YELLOW}{pila_1}{RESET}, Pila2: {MAGENTA}{pila_2}{RESET} Estado: {CYAN}{state}{RESET}")
                elif (letra == 'X' and pila_1[-1] == 'C'):
                    pila_1.append(letra)
                    del pila_2[-1]
                    state = 'q4'
                    
                    print(f"Transicion 11: Caracter: {GREEN}{letra}{RESET}, Pila1: {YELLOW}{pila_1}{RESET}, Pila2: {MAGENTA}{pila_2}{RESET} Estado: {CYAN}{state}{RESET}")
                elif (letra == 'X' and pila_1[-1] == 'V'):
                    pila_1.append(letra)
                    del pila_2[-1]
                    state = 'q4'
                    
                    print(f"Transicion 12: Caracter: {GREEN}{letra}{RESET}, Pila1: {YELLOW}{pila_1}{RESET}, Pila2: {MAGENTA}{pila_2}{RESET} Estado: {CYAN}{state}{RESET}")
                else:
                    return f"{RED}La expresión{RESET} {YELLOW}{expresion}{RESET} {RED}no pertenece a la gramática (Por F2){RESET}", state, pila_1, pila_2
            case 'q3':
                if (letra == 'C' and pila_1[-1] == 'O'):
                    pila_1.append(letra)
                    state = 'q3'
                    
                    print(f"Transicion 13: Caracter: {GREEN}{letra}{RESET}, Pila1: {YELLOW}{pila_1}{RESET}, Pila2: {MAGENTA}{pila_2}{RESET} Estado: {CYAN}{state}{RESET}")
                elif (letra == 'V' and pila_1[-1] == 'O'):
                    pila_1.append(letra)
                    state = 'q3'
                    
                    print(f"Transicion 14: Caracter: {GREEN}{letra}{RESET}, Pila1: {YELLOW}{pila_1}{RESET}, Pila2: {MAGENTA}{pila_2}{RESET} Estado: {CYAN}{state}{RESET}")
                elif (letra == 'O' and pila_1[-1] == 'V'):
                    pila_1.append(letra)
                    state = 'q3'
                    
                    print(f"Transicion 15: Caracter: {GREEN}{letra}{RESET}, Pila1: {YELLOW}{pila_1}{RESET}, Pila2: {MAGENTA}{pila_2}{RESET} Estado: {CYAN}{state}{RESET}")
                elif (letra == 'O' and pila_1[-1] == 'C'):
                    pila_1.append(letra)
                    state = 'q3'
                    
                    print(f"Transicion 16: Caracter: {GREEN}{letra}{RESET}, Pila1: {YELLOW}{pila_1}{RESET}, Pila2: {MAGENTA}{pila_2}{RESET} Estado: {CYAN}{state}{RESET}")
                elif (letra == 'Y' and pila_2[-1] == 'Pa'):
                    pila_2.append('Pa')
                    state = 'q3'
                    
                    print(f"Transicion 17: Caracter: {GREEN}{letra}{RESET}, Pila1: {YELLOW}{pila_1}{RESET}, Pila2: {MAGENTA}{pila_2}{RESET} Estado: {CYAN}{state}{RESET}")
                elif (letra == 'Z' and pila_2[-1] == 'Pa'):
                    del pila_2[-1]
                    state = 'q3'
                    
                    print(f"Transicion 18: Caracter: {GREEN}{letra}{RESET}, Pila1: {YELLOW}{pila_1}{RESET}, Pila2: {MAGENTA}{pila_2}{RESET} Estado: {CYAN}{state}{RESET}")
                elif (letra == 'Y' and pila_2[-1] == 'z0'):
                    pila_2.append('Pa')
                    state = 'q3'
                    
                    print(f"Transicion 19: Caracter: {GREEN}{letra}{RESET}, Pila1: {YELLOW}{pila_1}{RESET}, Pila2: {MAGENTA}{pila_2}{RESET} Estado: {CYAN}{state}{RESET}")
                elif (letra == 'X' and pila_1[-1] == 'C'):
                    pila_1.append(letra)
                    del pila_2[-1]
                    state = 'q4'
                    
                    print(f"Transicion 20: Caracter: {GREEN}{letra}{RESET}, Pila1: {YELLOW}{pila_1}{RESET}, Pila2: {MAGENTA}{pila_2}{RESET} Estado: {CYAN}{state}{RESET}")
                elif (letra == 'X' and pila_1[-1] == 'V'):
                    pila_1.append(letra)
                    del pila_2[-1]
                    state = 'q4'
                    
                    print(f"Transicion 21: Caracter: {GREEN}{letra}{RESET}, Pila1: {YELLOW}{pila_1}{RESET}, Pila2: {MAGENTA}{pila_2}{RESET} Estado: {CYAN}{state}{RESET}")
                else:
                    return f"{RED}La expresión{RESET} {YELLOW}{expresion}{RESET} {RED}no pertenece a la gramática (Por F2){RESET}", state, pila_1, pila_2
    
    return "", state, pila_1, pila_2

def automata_constantes_numericas(token: str, hex: list[str]) -> bool:
    """
    Autómata para validar las constantes numéricas de la expresion.

    Parameters
    ----------
    token : str
        Constante a evaluar por el autómata.
    hex : list[str]
        Lista de los números en hexadecimal.

    Returns
    -------
    bool : True si el token es válido, False en caso contrario.
    """
    # Estados del autómata de constan
    q0 = State("InitialS_q0")
    q1 = State("State_q1")
    q2 = State("FinalS_q2") # Para el número 0
    q3 = State("FinalS_q3") # Para el número decimal
    q4 = State("FinalS_q4") # Pare el número octal
    q5 = State("FinalS_q5") # Para el número hexadecimal
    q6 = State("FinalS_q6") # Para el número decimal sin exponente
    q7 = State("State_q7") 
    q8 = State("State_q8")
    q9 = State("FinalS_q9") # Para el número decimal con exponente de 1 carácter
    q10 = State("FinalS_q10") # Paara el número deciaml con exponente de 2 ces

    dfa_cn = DeterministicFiniteAutomaton()

    # Estado inicial y estados finales
    dfa_cn.add_start_state(q0)
    dfa_cn.add_final_state(q2)
    dfa_cn.add_final_state(q3)
    dfa_cn.add_final_state(q4)
    dfa_cn.add_final_state(q5)
    dfa_cn.add_final_state(q6)
    dfa_cn.add_final_state(q9)
    dfa_cn.add_final_state(q10)

    dfa_cn.add_transition(q0, '+', q1) # type: ignore
    dfa_cn.add_transition(q0, '-', q1) # type: ignore
    dfa_cn.add_transition(q0, '0', q2) # type: ignore
    dfa_cn.add_transition(q1, '0', q2) # type: ignore
    dfa_cn.add_transition(q2, '.', q6) # type: ignore
    dfa_cn.add_transition(q2, 'x', q5) # type: ignore
    dfa_cn.add_transition(q3, '.', q6) # type: ignore
    dfa_cn.add_transition(q6, 'E', q7) # type: ignore
    dfa_cn.add_transition(q7, '+', q8) # type: ignore
    dfa_cn.add_transition(q7, '-', q8) # type: ignore

    for c in range(1,10):
        dfa_cn.add_transition(q0, str(c), q3) # type: ignore
        dfa_cn.add_transition(q1, str(c), q3) # type: ignore

    for c in range(0,10):
        dfa_cn.add_transition(q3, str(c), q3) # type: ignore
        dfa_cn.add_transition(q5, str(c), q5) # type: ignore
        dfa_cn.add_transition(q7, str(c), q9) # type: ignore
        dfa_cn.add_transition(q6, str(c), q6) # type: ignore
        dfa_cn.add_transition(q8, str(c), q9) # type: ignore
        dfa_cn.add_transition(q9, str(c), q10) # type: ignore

    for c in range(0,8):
        dfa_cn.add_transition(q2, str(c), q4) # type: ignore
        dfa_cn.add_transition(q4, str(c), q4) # type: ignore

    for c in hex:
        dfa_cn.add_transition(q5, c, q5) # type: ignore

    return dfa_cn.accepts(token) # type: ignore

def automata_variables(token: str, variables: list[str]) -> bool:
    """
    Autómata para validar las constantes numéricas de la expresion.

    Parameters
    ----------
    token : str
        Constante a evaluar por el autómata.
    variables : list[str]
        Lista con los caracteres validos nombrar una variable.

    Returns
    -------
    bool : True si el token es válido, False en caso contrario.
    """
    q0 = State("InitialS_q0")
    q1 = State("FinalS_q1") # Variables de un solo carácter
    q2 = State("FinalS_q2") # Variables de más de un carácter

    dfa_v = DeterministicFiniteAutomaton()

    dfa_v.add_start_state(q0)
    dfa_v.add_final_state(q1)
    dfa_v.add_final_state(q2)

    for v in variables:
        dfa_v.add_transition(q0, v, q1) # type: ignore
        dfa_v.add_transition(q1, v, q2) # type: ignore
        dfa_v.add_transition(q2, v, q2) # type: ignore

    for c in range(0,10):
        dfa_v.add_transition(q1, str(c), q2) # type: ignore
        dfa_v.add_transition(q2, str(c), q2) # type: ignore

    return dfa_v.accepts(token) # type: ignore