# Práctica 3. Gramáticas independientes del contexto
# Integrantes: García Escamilla Bryan Alexis y Melendez Macedonio Rodrigo 

from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State
import nltk
from nltk import CFG

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

# <--------------------ESTADOS PARA EL AUTÓMATA DE OPERADORES/ASIGNACIONES-------------------->

# Definimos los estados
s0 = State("Estado_Inicial_S0") # Estado inicial del autómata
s1 = State("Estado_S1")
s2 = State("Estado_S2")
s3 = State("Estado_Final_S3") # Estado de acepatción para VOV,VOC,VOY,VAV,VAC,VAY,COV,COC,COY,ZOY,ZOV,ZOC
s4 = State("Estado_S4")

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

BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_MAGENTA = "\033[95m"
RESET = "\033[0m"

# <--------------------FUNCIONES NECESARIAS PARA EL PROGRAMA-------------------->

# <--------------------FUNCIÓN PARA MOSTRAR EL ÁRBOL DE DERIVACIÓN-------------------->

def Arbol_Derivacion(Cadena_Aux):
    # Definir la gramática
    Gramatica = CFG.fromstring("""
    S -> A ';' | ';'
    A -> A '(' A ')' | '(' ')' | '(' A ')' | A '(' ')'
    """)

    # Crear el parser
    Parser = nltk.ChartParser(Gramatica)

    # Tokenizar la oración
    Tokens = nltk.word_tokenize(Cadena_Aux)

    # Intentar parsear y mostrar los árboles de análisis
    try:
        Encontrar_Parse = False
        for Tree in Parser.parse(Tokens):
            Encontrar_Parse = True
            print("Árbol de derivación:")
            print("")
            Tree.pretty_print()
        
        if not Encontrar_Parse:
            print("No se encontraron árboles de derivación válidos.")

    except ValueError as Error:
        print(f"No se puede analizar la oración: {Error}")

# <--------------------AUTÓMATA DE PILA PARA VALIDAR LOS PARÉNTESIS-------------------->

def Automata_Pila_Parentesis(Expresion,Cadena_Aux,Estado,Pila):
    print("Proceso de validación de la expresión: ")
    print("")
    for Letra in Cadena_Aux:    
        if Estado == 'e0':
            if Letra == '(' and Pila[-1] == 'z0':
                Pila.append('Pa')
                Estado = 'e0'
                print(f"Transicion 1: Caracter: {BRIGHT_MAGENTA}{Letra}{RESET}, Pila: {BRIGHT_BLUE}{Pila}{RESET}, Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            elif Letra == '(' and Pila[-1] == 'Pa':
                Pila.append('Pa')
                Estado = 'e0'
                print(f"Transicion 2: Caracter: {BRIGHT_MAGENTA}{Letra}{RESET}, Pila: {BRIGHT_BLUE}{Pila}{RESET}, Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            elif Letra == ')' and Pila[-1] == 'Pa':
                del Pila[-1]
                Estado = "e0"
                print(f"Transicion 3: Caracter: {BRIGHT_MAGENTA}{Letra}{RESET}, Pila: {BRIGHT_BLUE}{Pila}{RESET}, Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            elif Letra == ';' and Pila[-1] == 'z0':
                del Pila[-1]
                Estado = 'e1'
                print(f"Transicion 4: Caracter: {BRIGHT_MAGENTA}{Letra}{RESET}, Pila: {BRIGHT_BLUE}{Pila}{RESET}, Estado: {BRIGHT_CYAN}{Estado}{RESET}")
            else:
                print("")
                return f"{BRIGHT_RED}La expresión{RESET} {BRIGHT_YELLOW}{Expresion}{RESET} {BRIGHT_RED}no pertenece a la gramática (Por F2){RESET}",Estado,Pila
    return "",Estado,int(len(Pila))

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

# <--------------------AUTÓMATA PARA OPERADORES/ASIGNACIONES-------------------->

# Creamos el DFA_Comparadores_Operadores_Asignaciones
DFA_Operadores_Asignaciones = DeterministicFiniteAutomaton()

# Añadimos el estado inicial y los estados finales al DFA_Comparadores_Operadores_Asignaciones
DFA_Operadores_Asignaciones.add_start_state(s0)
DFA_Operadores_Asignaciones.add_final_state(s3)

# Añadimos las transiciones al DFA_Comparadores_Operadores_Asignaciones
    
# Transiciones para s0
DFA_Operadores_Asignaciones.add_transition(s0,"V",s1)
DFA_Operadores_Asignaciones.add_transition(s0,"C",s4)
DFA_Operadores_Asignaciones.add_transition(s0,"Z",s4)

# Transiciones para s1
DFA_Operadores_Asignaciones.add_transition(s1,"O",s2)
DFA_Operadores_Asignaciones.add_transition(s1,"A",s2)

# Transiciones para s2
DFA_Operadores_Asignaciones.add_transition(s2,"V",s3)
DFA_Operadores_Asignaciones.add_transition(s2,"C",s3)
DFA_Operadores_Asignaciones.add_transition(s2,"Y",s3)

# Transiciones para s4
DFA_Operadores_Asignaciones.add_transition(s4,"O",s2)

# Verificamos si una cadena es aceptada por el DFA_Comparadores_Operadores_Asignaciones
def Validar_Operador_Clasificacion(Cadena_Aux):
    return DFA_Operadores_Asignaciones.accepts(Cadena_Aux)

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

# <--------------------SE CLASIFICA CADA UNO DE LOS TOKENS DE LA EXPRESIÓN ASIGNANDOLES UNA LETRA-------------------->

Clasificaciones_Expresion = [] # Lista donde se clasifican a los tokens de la expresión
Llave = 0 # Llave para pasar del filtro 1 al filtro 2

for Token in Expresion_Lista:
    if Token.isalpha() == True and Token in Palabras_Reservadas_C: # Si el token es una palabra reservada
        if Token in Palabras_Reservadas_C_VN: # Si el token es una palabra reservada con valor numérico
            Clasificaciones_Expresion.append('H')
        else: # Si el token es una palabra reservada pero no con valor numérico 
            Clasificaciones_Expresion.append('P')
    else: # Si el token no es una palabra reservada
        if Token.startswith(('0','1','2','3','4','5','6','7','8','9','+','-')): # Si el token es un número
            if Validar_Constante_Numerica(Token) == True: # Si el token es una constante numérica
                Clasificaciones_Expresion.append('C')
            else: # Si el token no es una constante numérica
                if Token == '+' or Token == '-': # Si el token es un operador
                    Clasificaciones_Expresion.append('O')
                else: # Si el token es una constante numérica y esta mal
                    Clasificaciones_Expresion.append('M')
                    Llave = 1 # El segundo filtro se cierra
        else:
            if Validar_Variables(Token) == True: # Si el token es una variable
                Clasificaciones_Expresion.append('V')
            else: # Si el token no es una variable
                if Token == '/' or Token == '*' or Token == '%': # Si el token es un operador
                    Clasificaciones_Expresion.append('O')
                elif Token == '=': # Si el token es un signo de asignación
                    Clasificaciones_Expresion.append('A')
                elif Token == '(': # Si el token es un paréntesis de apertura
                    Clasificaciones_Expresion.append('Y')
                elif Token == ')': # Si el token es un paréntesis de cierre
                    Clasificaciones_Expresion.append('Z')
                elif Token == ';': # Si el token es un punto y coma
                    Clasificaciones_Expresion.append('X')
                else: # Si es una variable incorrecta
                    if (Token in Signos_Invalidos) == True:
                        Llave = 1
                    else:
                        if Validar_Variables(Token) == False: # Si el token es una variable incorrecta 
                            Clasificaciones_Expresion.append('W')
                            Llave = 1 # El segundo filtro se cierra

print(f"La Clasificaciones_Expresion es: {Clasificaciones_Expresion}")

# <--------------------PRIMER FILTRO-------------------->

# <--------------------VALIDAMOS LOS COMPARADORES/OPERADORES/ASIGNACIONES-------------------->

Cadena_Aux = "" # Cadena auxiliar para concatenar y para mandar a validar

if Clasificaciones_Expresion[0] == 'V' and Clasificaciones_Expresion[1] == 'A' and Clasificaciones_Expresion[-1] == 'X':
    for Posicion_Token in range(0,len(Clasificaciones_Expresion)):

        if Clasificaciones_Expresion[Posicion_Token] == 'O':
            Cadena_Aux = Clasificaciones_Expresion[Posicion_Token - 1] + Clasificaciones_Expresion[Posicion_Token] + Clasificaciones_Expresion[Posicion_Token + 1]
            if Validar_Operador_Clasificacion(Cadena_Aux) == False:
                Llave = 1 # El segundo filtro se cierra
            Cadena_Aux = ""
        if Clasificaciones_Expresion[Posicion_Token] == 'A':
            Cadena_Aux = Clasificaciones_Expresion[Posicion_Token - 1] + Clasificaciones_Expresion[Posicion_Token] + Clasificaciones_Expresion[Posicion_Token + 1]
            if Validar_Operador_Clasificacion(Cadena_Aux) == False:
                Llave = 1 # El segundo filtro se cierra
            Cadena_Aux = ""
else:
    Llave = 1 # El segundo filtro se cierra

# <--------------------SEGUNDO FILTRO-------------------->
if Llave == 0: # El segundo filtro se abre
    Estado = 'e0'
    Pila = ['z0']
    Cadena_Aux = ""

    for Token in Expresion:
        if Token == '(' or Token == ')' or Token == ';':
            Cadena_Aux = Cadena_Aux + Token
    
    print(f"La Cadena_Aux es: {Cadena_Aux}")
    print("")
    
    # Se manda a validar al automata de pila
    Mensaje,Estado,Pila = Automata_Pila_Parentesis(Expresion,Cadena_Aux,Estado,Pila)
        
    if Mensaje != "":
        print(Mensaje)
    else:
        if Estado == 'e1' or Pila == 0:
            print("")
            print(f"{BRIGHT_GREEN}La expresión{RESET} {BRIGHT_YELLOW}{Expresion}{RESET} {BRIGHT_GREEN}pertenece a la gramática (Por F2){RESET}")
            print("")
            Arbol_Derivacion(Cadena_Aux)
        elif Estado != 'e1' or Pila != 0:
            print("")
            print(f"{BRIGHT_RED}La expresión{RESET} {BRIGHT_YELLOW}{Expresion}{RESET} {BRIGHT_RED}no pertenece a la gramática (Por F2){RESET}") 
else: # El segundo filtro permanece cerrado
    print("")
    print(f"{BRIGHT_RED}La expresión{RESET} {BRIGHT_YELLOW}{Expresion}{RESET} {BRIGHT_RED}no pertenece a la gramática (Por F1){RESET}")