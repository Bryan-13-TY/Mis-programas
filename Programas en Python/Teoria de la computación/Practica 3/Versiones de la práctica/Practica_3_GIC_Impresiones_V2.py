# Práctica 3. Gramáticas independientes del contexto
# Integrantes: García Escamilla Bryan Alexis y Melendez Macedonio Rodrigo 

from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State

# <--------------------ESTADOS PARA EL AUTÓMATA DE CONSTANTES NUMÉRICAS-------------------->

# Definimos los estados
q0 = State("Estado_Inicial_Q0") # Estado inicial del autómata
q1 = State("Estado_Q1")
q2 = State("Estado_Final_Q2") # Estado de aceptación cuando el número es 0
q3 = State("Estado_Final_Q3") # Estado de aceptacion cuando el número es decimal
q4 = State("Estado_Final_Q4") # Estado de aceptación cuando el número es octal
q5 = State("Estado_Final_Q5") # Estado de aceptación cuando el número es hexadecimal
q6 = State("Estado_Final_Q6") # Estado de aceptación cuando el núemro es decimal sin exponente
q7 = State("Estado_Q7") 
q8 = State("Estado_Q8")
q9 = State("Estado_Final_Q9") # Estado de aceptación cuando el número es decimal con exponente de 1 caracter
q10 = State("Estado_Final_Q10") # Estado de aceptación cuando el número es decimal con exponente de 2 caracteres

# <--------------------ESTADOS PARA EL AUTÓMATA DE VARIABLES-------------------->

# Definimos los estados
r0 = State("Estado_Inicial_R0") # Estado inicial del autómata
r1 = State("Estado_Final_R1") # Estado de aceptación para las variables de un solo caracter
r2 = State("Estado_Final_R2") # Estado de aceptación para las variables de más de un caracter

# <--------------------ALFABETOS NECESARIOS PARA EL PROGRAMA-------------------->

Letras_Hex = ['A','B','C','D','E','F']

Caracteres_Variables = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o','p','q','r','s','t','u','v','w','x','y','z'
                        ,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z'
                        ,'_','$']

Signos_Invalidos = [',','{','}','[',']','','"',"'",'|','°','¬','^','¨','?','¡','¿','$','#','.','~','´']

Palabras_Reservadas_C = ['auto','break','case','char','const','continue','default','do','double','else'
                         ,'enum','extern','float','for','goto','if','inline','int','long','register'
                         ,'restrict','return','short','signed','sizeof','static','struct','switch','typedef','union'
                         ,'unsigned','void','volatile','while','_Alignas','_Alignof','_Atomic','_Bool','_Complex','Decimal128'
                         ,'_Decimal32','_Decimal64','_Generic','_Imaginary','_Noreturn','_Static_assert','_Thread_local']

Palabras_Reservadas_C_VN = ['char','short','int','long','float','double','asigned','unsigned','_Bool','_Complex'
                            '_Decimal32','_Decimal64','_Decimal128']

# <--------------------CÓDIGOS DE COLOR ANSI-------------------->

MAGENTA = "\033[35m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_MAGENTA = "\033[95m"
RESET = "\033[0m"

# <--------------------FUNCIONES NECESARIAS PARA EL PROGRAMA-------------------->

# <--------------------AUTÓMATA DE PILA PARA VALIDAR EL ORDEN DE LOS PARÉNTESIS,VARIABLES,CONSTANTES,OPERADORES,ASIGNACIONES-------------------->

def Automata_Pila(Expresion,Expresion_Evaluar,Estado,Pila1,Pila2):
    print("Proceso de validación de la expresión: ")
    print("")
    for Letra in Expresion_Evaluar:
        if Estado == 'q0':
            if Letra == 'V' and Pila1[-1] == 'z0':
                Pila1.append('V')
                Estado = 'q1'
                print(f"Transicion 1: Caracter: {BRIGHT_GREEN}{Letra}{RESET}, Pila1: {BRIGHT_YELLOW}{Pila1}{RESET}, Pila2: {BRIGHT_MAGENTA}{Pila2}{RESET} Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            else:
                return f"{BRIGHT_RED}La expresión{RESET} {BRIGHT_YELLOW}{Expresion}{RESET} {BRIGHT_RED}no pertenece a la gramática{RESET}",Estado,Pila1,Pila2
        elif Estado == 'q1':
            if Letra == 'A' and Pila1[-1] == 'V':
                Pila1.append('A')
                Estado = 'q2'
                print(f"Transicion 2: Caracter: {BRIGHT_GREEN}{Letra}{RESET}, Pila1: {BRIGHT_YELLOW}{Pila1}{RESET}, Pila2: {BRIGHT_MAGENTA}{Pila2}{RESET} Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            else:
                return f"{BRIGHT_RED}La expresión{RESET} {BRIGHT_YELLOW}{Expresion}{RESET} {BRIGHT_RED}no pertenece a la gramática{RESET}",Estado,Pila1,Pila2
        elif Estado == 'q2':
            if Letra == 'V' and Pila1[-1] == 'A':
                Pila1.append('V')
                Estado = 'q2'
                print(f"Transicion 3: Caracter: {BRIGHT_GREEN}{Letra}{RESET}, Pila1: {BRIGHT_YELLOW}{Pila1}{RESET}, Pila2: {BRIGHT_MAGENTA}{Pila2}{RESET} Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            elif Letra == 'C' and Pila1[-1] == 'A':
                Pila1.append('C')
                Estado = 'q2'
                print(f"Transicion 4: Caracter: {BRIGHT_GREEN}{Letra}{RESET}, Pila1: {BRIGHT_YELLOW}{Pila1}{RESET}, Pila2: {BRIGHT_MAGENTA}{Pila2}{RESET} Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            elif Letra == 'Y' and Pila2[-1] == 'z0':
                Pila2.append('Pa')
                Estado = 'q2'
                print(f"Transicion 5: Caracter: {BRIGHT_GREEN}{Letra}{RESET}, Pila1: {BRIGHT_YELLOW}{Pila1}{RESET}, Pila2: {BRIGHT_MAGENTA}{Pila2}{RESET} Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            elif Letra == 'Z' and Pila2[-1] == 'Pa':
                del Pila2[-1]
                Estado = 'q2'
                print(f"Transicion 6: Caracter: {BRIGHT_GREEN}{Letra}{RESET}, Pila1: {BRIGHT_YELLOW}{Pila1}{RESET}, Pila2: {BRIGHT_MAGENTA}{Pila2}{RESET} Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            elif Letra == 'Y' and Pila2[-1] == 'Pa':
                Pila2.append('Pa')
                Estado = 'q2'
                print(f"Transicion 7: Caracter: {BRIGHT_GREEN}{Letra}{RESET}, Pila1: {BRIGHT_YELLOW}{Pila1}{RESET}, Pila2: {BRIGHT_MAGENTA}{Pila2}{RESET} Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            elif Letra == 'A' and Pila1[-1] == 'V':
                Pila1.append('A')
                Estado = 'q2'
                print(f"Transicion 8: Caracter: {BRIGHT_GREEN}{Letra}{RESET}, Pila1: {BRIGHT_YELLOW}{Pila1}{RESET}, Pila2: {BRIGHT_MAGENTA}{Pila2}{RESET} Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            elif Letra == 'O' and Pila1[-1] == 'V':
                Pila1.append('O')
                Estado = 'q3'
                print(f"Transicion 9: Caracter: {BRIGHT_GREEN}{Letra}{RESET}, Pila1: {BRIGHT_YELLOW}{Pila1}{RESET}, Pila2: {BRIGHT_MAGENTA}{Pila2}{RESET} Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            elif Letra == 'O' and Pila1[-1] == 'C':
                Pila1.append('O')
                Estado = 'q3'
                print(f"Transicion 10: Caracter: {BRIGHT_GREEN}{Letra}{RESET}, Pila1: {BRIGHT_YELLOW}{Pila1}{RESET}, Pila2: {BRIGHT_MAGENTA}{Pila2}{RESET} Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            elif Letra == 'X' and Pila1[-1] == 'C':
                Pila1.append('X')
                del Pila2[-1]
                Estado = 'q4'
                print(f"Transicion 11: Caracter: {BRIGHT_GREEN}{Letra}{RESET}, Pila1: {BRIGHT_YELLOW}{Pila1}{RESET}, Pila2: {BRIGHT_MAGENTA}{Pila2}{RESET} Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            elif Letra == 'X' and Pila1[-1] == 'V':
                Pila1.append('X')
                del Pila2[-1]
                Estado = 'q4'
                print(f"Transicion 12: Caracter: {BRIGHT_GREEN}{Letra}{RESET}, Pila1: {BRIGHT_YELLOW}{Pila1}{RESET}, Pila2: {BRIGHT_MAGENTA}{Pila2}{RESET} Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            else:
                return f"{BRIGHT_RED}La expresión{RESET} {BRIGHT_YELLOW}{Expresion}{RESET} {BRIGHT_RED}no pertenece a la gramática{RESET}",Estado,Pila1,Pila2
        elif Estado == 'q3':
            if Letra == 'C' and Pila1[-1] == 'O':
                Pila1.append('C')
                Estado = 'q3'
                print(f"Transicion 13: Caracter: {BRIGHT_GREEN}{Letra}{RESET}, Pila1: {BRIGHT_YELLOW}{Pila1}{RESET}, Pila2: {BRIGHT_MAGENTA}{Pila2}{RESET} Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            elif Letra == 'V' and Pila1[-1] == 'O':
                Pila1.append('V')
                Estado = 'q3'
                print(f"Transicion 14: Caracter: {BRIGHT_GREEN}{Letra}{RESET}, Pila1: {BRIGHT_YELLOW}{Pila1}{RESET}, Pila2: {BRIGHT_MAGENTA}{Pila2}{RESET} Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            elif Letra == 'O' and Pila1[-1] == 'V':
                Pila1.append('O')
                Estado = 'q3'
                print(f"Transicion 15: Caracter: {BRIGHT_GREEN}{Letra}{RESET}, Pila1: {BRIGHT_YELLOW}{Pila1}{RESET}, Pila2: {BRIGHT_MAGENTA}{Pila2}{RESET} Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            elif Letra == 'O' and Pila1[-1] == 'C':
                Pila1.append('O')
                Estado = 'q3'
                print(f"Transicion 16: Caracter: {BRIGHT_GREEN}{Letra}{RESET}, Pila1: {BRIGHT_YELLOW}{Pila1}{RESET}, Pila2: {BRIGHT_MAGENTA}{Pila2}{RESET} Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            elif Letra == 'Y' and Pila2[-1] == 'Pa':
                Pila2.append('Pa')
                Estado == 'q3'
                print(f"Transicion 17: Caracter: {BRIGHT_GREEN}{Letra}{RESET}, Pila1: {BRIGHT_YELLOW}{Pila1}{RESET}, Pila2: {BRIGHT_MAGENTA}{Pila2}{RESET} Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            elif Letra == 'Z' and Pila2[-1] == 'Pa':
                del Pila2[-1]
                Estado = 'q3'
                print(f"Transicion 18: Caracter: {BRIGHT_GREEN}{Letra}{RESET}, Pila1: {BRIGHT_YELLOW}{Pila1}{RESET}, Pila2: {BRIGHT_MAGENTA}{Pila2}{RESET} Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            elif Letra == 'Y' and Pila2[-1] == 'z0':
                Pila2.append('Pa')
                Estado = 'q3'
                print(f"Transicion 19: Caracter: {BRIGHT_GREEN}{Letra}{RESET}, Pila1: {BRIGHT_YELLOW}{Pila1}{RESET}, Pila2: {BRIGHT_MAGENTA}{Pila2}{RESET} Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            elif Letra == 'X' and Pila1[-1] == 'C':
                Pila1.append('X')
                del Pila2[-1]
                Estado = 'q4'
                print(f"Transicion 20: Caracter: {BRIGHT_GREEN}{Letra}{RESET}, Pila1: {BRIGHT_YELLOW}{Pila1}{RESET}, Pila2: {BRIGHT_MAGENTA}{Pila2}{RESET} Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            elif Letra == 'X' and Pila1[-1] == 'V':
                Pila1.append('X')
                del Pila2[-1]
                Estado = 'q4'
                print(f"Transicion 21: Caracter: {BRIGHT_GREEN}{Letra}{RESET}, Pila1: {BRIGHT_YELLOW}{Pila1}{RESET}, Pila2: {BRIGHT_MAGENTA}{Pila2}{RESET} Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            else:
                return f"{BRIGHT_RED}La expresión{RESET} {BRIGHT_YELLOW}{Expresion}{RESET} {BRIGHT_RED}no pertenece a la gramática{RESET}",Estado,Pila1,Pila2
    return "",Estado,int(len(Pila1)),int(len(Pila2))  

# <--------------------AUTÓMATA PARA CONSTANTES NUMÉRICAS-------------------->

# Creamos el DFA_Constantes_Numericas
DFA_Constantes_Numericas = DeterministicFiniteAutomaton()

# Añadimos el estado inicial y los estados finales al DFA_Constantes_Numericas
DFA_Constantes_Numericas.add_start_state(q0)
DFA_Constantes_Numericas.add_final_state(q2)
DFA_Constantes_Numericas.add_final_state(q3)
DFA_Constantes_Numericas.add_final_state(q4)
DFA_Constantes_Numericas.add_final_state(q5)
DFA_Constantes_Numericas.add_final_state(q6)
DFA_Constantes_Numericas.add_final_state(q9)
DFA_Constantes_Numericas.add_final_state(q10)

# Añadimos las transiciones al DFA_Constantes_Numericas

# Transiciones para q0
DFA_Constantes_Numericas.add_transition(q0,"+",q1)
DFA_Constantes_Numericas.add_transition(q0,"-",q1)
DFA_Constantes_Numericas.add_transition(q0,"0",q2)
for Caracter in range(1,10):
    DFA_Constantes_Numericas.add_transition(q0,str(Caracter),q3)

# Transiciones para q1
DFA_Constantes_Numericas.add_transition(q1,"0",q2)
for Caracter in range(1,10):
    DFA_Constantes_Numericas.add_transition(q1,str(Caracter),q3)

# Transiciones para q2
DFA_Constantes_Numericas.add_transition(q2,".",q6)
for Caracter in range(0,8):
    DFA_Constantes_Numericas.add_transition(q2,str(Caracter),q4)
DFA_Constantes_Numericas.add_transition(q2,"x",q5)

# Transiciones para q3
DFA_Constantes_Numericas.add_transition(q3,".",q6)
for Caracter in range(0,10):
    DFA_Constantes_Numericas.add_transition(q3,str(Caracter),q3)

# Transiciones para q4
for Caracter in range(0,8):
    DFA_Constantes_Numericas.add_transition(q4,str(Caracter),q4)

# Transiciones para q5
for Caracter in range(0,10):
    DFA_Constantes_Numericas.add_transition(q5,str(Caracter),q5)

for Caracter in Letras_Hex:
    DFA_Constantes_Numericas.add_transition(q5,Caracter,q5)

# Transiciones para q6
for Caracter in range(0,10):
    DFA_Constantes_Numericas.add_transition(q6,str(Caracter),q6)
DFA_Constantes_Numericas.add_transition(q6,"E",q7)

# Transiciones para q7
DFA_Constantes_Numericas.add_transition(q7,"+",q8)
DFA_Constantes_Numericas.add_transition(q7,"-",q8)
for Caracter in range(0,10):
    DFA_Constantes_Numericas.add_transition(q7,str(Caracter),q9)

# Transiciones para q8
for Caracter in range(0,10):
    DFA_Constantes_Numericas.add_transition(q8,str(Caracter),q9)

# Transiciones para q9
for Caracter in range(0,10):
    DFA_Constantes_Numericas.add_transition(q9,str(Caracter),q10)

# Verificamos si un token es aceptado por el DFA_Constantes_Numericas
def Validar_Constante_Numerica(Token):
    return DFA_Constantes_Numericas.accepts(Token)

# <--------------------AUTÓMATA PARA LAS VARIABLES-------------------->

# Creamos el DFA_Variables
DFA_Variables = DeterministicFiniteAutomaton()

# Añadimos el estado inicial y los estados finales al DFA_Variables
DFA_Variables.add_start_state(r0)
DFA_Variables.add_final_state(r1)
DFA_Variables.add_final_state(r2)

# Añadimos las transiciones al DFA_Variables

# Transiciones para r0
for Caracter in Caracteres_Variables:
    DFA_Variables.add_transition(r0,Caracter,r1)

# Transiciones para r1 y r2
for Caracter in Caracteres_Variables:
    DFA_Variables.add_transition(r1,Caracter,r2)
    DFA_Variables.add_transition(r2,Caracter,r2)
for Caracter in range(0,10):
    DFA_Variables.add_transition(r1,str(Caracter),r2)
    DFA_Variables.add_transition(r2,str(Caracter),r2)

# Verificamos si un token es aceptado por el DFA_Variables
def Validar_Variables(Token):
    return DFA_Variables.accepts(Token)

# <--------------------SE CLASIFICA CADA TOKEN DE LA EXPRESIÓN-------------------->

Expresion = input("Ingresa una expresión: ")
Expresion_Lista = Expresion.split(" ") # Lista donde se guardan los tokens de la expresión

print(f"La Expresion_Lista es: {Expresion_Lista}")

# <--------------------NOMENCLATURA PARA CADA TOKEN DEL ARCHIVO-------------------->

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

# <--------------------PRIMER FILTRO-------------------->

# <--------------------SE CLASIFICA CADA UNO DE LOS TOKENS DE LA EXPRESIÓN ASIGNANDOLES UNA LETRA-------------------->

Expresion_Evaluar = "" # Lista donde se clasifican a los tokens de la expresión
Llave = 0 # Llave para pasar del filtro 1 al filtro 2

for Token in Expresion_Lista:
    if Token.isalpha() == True and Token in Palabras_Reservadas_C: # Si el token es una palabra reservada
        if Token in Palabras_Reservadas_C_VN: # Si el token es una palabra reservada con valor numérico
            Expresion_Evaluar = Expresion_Evaluar + 'H'
        else: # Si el token es una palabra reservada pero no con valor numérico 
            Expresion_Evaluar = Expresion_Evaluar + 'P'
    else: # Si el token no es una palabra reservada
        if Token.startswith(('0','1','2','3','4','5','6','7','8','9','+','-')): # Si el token es un número
            if Validar_Constante_Numerica(Token) == True: # Si el token es una constante numérica
                Expresion_Evaluar = Expresion_Evaluar + 'C'
            else: # Si el token no es una constante numérica
                if Token == '+' or Token == '-': # Si el token es un operador
                    Expresion_Evaluar = Expresion_Evaluar + 'O'
                else: # Si el token es una constante numérica y esta mal
                    Expresion_Evaluar = Expresion_Evaluar + 'M'
                    Llave = 1 # El segundo filtro se cierra
        else:
            if Validar_Variables(Token) == True: # Si el token es una variable
                Expresion_Evaluar = Expresion_Evaluar + 'V'
            else: # Si el token no es una variable
                if Token == '/' or Token == '*' or Token == '%': # Si el token es un operador
                    Expresion_Evaluar = Expresion_Evaluar + 'O'
                elif Token == '=': # Si el token es un signo de asignación
                    Expresion_Evaluar = Expresion_Evaluar + 'A'
                elif Token == '(': # Si el token es un paréntesis de apertura
                    Expresion_Evaluar = Expresion_Evaluar + 'Y'
                elif Token == ')': # Si el token es un paréntesis de cierre
                    Expresion_Evaluar = Expresion_Evaluar + 'Z'
                elif Token == ';': # Si el token es un punto y coma
                    Expresion_Evaluar = Expresion_Evaluar + 'X'
                else: # Si es una variable incorrecta
                    if (Token in Signos_Invalidos) == True:
                        Llave = 1
                    else:
                        if Validar_Variables(Token) == False: # Si el token es una variable incorrecta
                            Expresion_Evaluar = Expresion_Evaluar + 'W' 
                            Llave = 1 # El segundo filtro se cierra

print(f"La Expresion_Evaluar es: {Expresion_Evaluar}")

# <--------------------SEGUNDO FILTRO-------------------->

if Llave == 0: # El segundo filtro se abre
    Estado = 'q0'
    Pila1 = ['z0'] # Pila para validar el orden de los operadores,variables,constantes y asignaciones
    Pila2 = ['z0'] # Pila para validar el orde de los paréntesis 
    
    # Se manda a validar al automata de pila
    Mensaje,Estado,Pila1,Pila2 = Automata_Pila(Expresion,Expresion_Evaluar,Estado,Pila1,Pila2)
        
    if Mensaje != "":
        print(Mensaje)
    else:
        if Estado == 'q4' and Pila2 == 0:
            print("")
            print(f"{BRIGHT_GREEN}La expresión{RESET} {BRIGHT_YELLOW}{Expresion}{RESET} {BRIGHT_GREEN}pertenece a la gramática (Por F2){RESET}")
        elif Estado != 'q4' and Pila2 != 0:
            print("")
            print(f"{BRIGHT_RED}La expresión{RESET} {BRIGHT_YELLOW}{Expresion}{RESET} {BRIGHT_RED}no pertenece a la gramática (Por F2){RESET}")
        elif Estado != 'q4' or Pila2 != 0:
            print("")
            print(f"{BRIGHT_RED}La expresión{RESET} {BRIGHT_YELLOW}{Expresion}{RESET} {BRIGHT_RED}no pertenece a la gramática (Por F2){RESET}")

else: # El segundo filtro permanece cerrado
    print("")
    print(f"{BRIGHT_RED}La expresión{RESET} {BRIGHT_YELLOW}{Expresion}{RESET} {BRIGHT_RED}no pertenece a la gramática (Por F1){RESET}")