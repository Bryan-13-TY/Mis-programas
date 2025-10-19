# Práctica 2. Analizador Léxico (Con impresiones)
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

# <--------------------ESTADOS PARA EL AUTÓMATA DE COMPARADORES/OPERADORES/ASIGNACIONES-------------------->

# Definimos los estados
s0 = State("Estado_Inicial_S0") # Estado inicial del autómata
s1 = State("Estado_S1")
s2 = State("Estado_S2")
s3 = State("Estado_Final_S3") # Estado de acepatción para VOV,VRV,VOC,VRC
s4 = State("Estado_S4")
s5 = State("Estado_S5")
s6 = State("Estado_S6")
s7 = State("Estado_S7")
s8 = State("Estado_Final_S8") # Estado de aceptación para VAYHZC
s9 = State("Estado_Final_S9") # Estado de aceptación para VAV,VAC
s10 = State("Estado_S10")
s11 = State("Estado_S11") 
s12 = State("Estado_Final_S12") # Estado de aceptación para COV,CRV,COC,CRC

# <--------------------ESTADOS PARA EL AUTÓMATA DE COMENTARIOS VL/UL-------------------->

#Definimos los estados
t0 = State("Estado_Inicial_T0") # Estado inicial del autómata
t1 = State("Estado_T1")
t2 = State("Estado_Final_T2") # Estado de acepatción para el comentario de varias lineas
t3 = State("Estado_Final_T3") # Estado de aceptación para el comentario de una linea

# <--------------------ALFABETOS NECESARIOS PARA EL PROGRAMA-------------------->

Letras_Hex = ['A','B','C','D','E','F']

Caracteres_Variables = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o','p','q','r','s','t','u','v','w','x','y','z'
                        ,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z'
                        ,'_','$']

Signos_Ignorados = [';',',','{','}','[',']','','"']

Palabras_Reservadas_Java = ['abstract','assert','boolean','break','byte','case','catch','char','class','const'
                            ,'continue','default','do','double','else','enum','extends','final','finally','float'
                            ,'for','goto','if','implements','import','instanceof','int','interface','long','main'
                            ,'native','new','null','package','private','protected','public','return','short','static'
                            ,'strictfp','super','switch','synchronized','this','throw','throws','transient','try','void'
                            ,'volatile','while']

Palabras_Reservadas_Java_VN = ['byte','double','float','int','long','short']


Clasificaciones_Comentarios_UL = ['C','M','V','P','O','R','S','A','Y','Z','H']

# <--------------------FUNCIONES NECESARIAS PARA EL PROGRAMA-------------------->

# Función para validar comparadores, operadores y asignaciones
def Validar_Comparador_Operador_Clasificacion_F(Cadena_Aux,Numero_Linea,Lineas_Con_Errores):
    if Validar_Comparador_Operador_Clasificacion(Cadena_Aux) == False:
                    if ((Numero_Linea + 1) in Lineas_Con_Errores) == False:
                        Lineas_Con_Errores.append(Numero_Linea + 1) # Se agrega el número de la linea con el error

# Función para validaar comentarios
def Validar_Comentarios_VL_UL_F(Cadena_Aux,Lista_Comentarios,Lineas_Con_Errores):
    if Validar_Comentarios_VL_UL(Cadena_Aux) == False:
                for Linea in Lista_Comentarios:
                    if (Linea in Lineas_Con_Errores) == False:
                        Lineas_Con_Errores.append(Linea) # Se agrega el número de la linea con el error

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

# <--------------------AUTÓMATA PARA COMPARADORES/OPERADORES/ASIGNACIONES-------------------->

# Creamos el DFA_Comparadores_Operadores_Asignaciones
DFA_Comparadores_Operadores_Asignaciones = DeterministicFiniteAutomaton()

# Añadimos el estado inicial y los estados finales al DFA_Comparadores_Operadores_Asignaciones
DFA_Comparadores_Operadores_Asignaciones.add_start_state(s0)
DFA_Comparadores_Operadores_Asignaciones.add_final_state(s3)
DFA_Comparadores_Operadores_Asignaciones.add_final_state(s8)
DFA_Comparadores_Operadores_Asignaciones.add_final_state(s9)
DFA_Comparadores_Operadores_Asignaciones.add_final_state(s12)

# Añadimos las transiciones al DFA_Comparadores_Operadores_Asignaciones
    
# Transiciones para s0
DFA_Comparadores_Operadores_Asignaciones.add_transition(s0,"V",s1)
DFA_Comparadores_Operadores_Asignaciones.add_transition(s0,"C",s10)

# Transiciones para s1
DFA_Comparadores_Operadores_Asignaciones.add_transition(s1,"O",s2)
DFA_Comparadores_Operadores_Asignaciones.add_transition(s1,"R",s2)
DFA_Comparadores_Operadores_Asignaciones.add_transition(s1,"A",s4)

# Transiciones para s2
DFA_Comparadores_Operadores_Asignaciones.add_transition(s2,"V",s3)
DFA_Comparadores_Operadores_Asignaciones.add_transition(s2,"C",s3)

# Transiciones para s4
DFA_Comparadores_Operadores_Asignaciones.add_transition(s4,"Y",s5)
DFA_Comparadores_Operadores_Asignaciones.add_transition(s4,"C",s9)
DFA_Comparadores_Operadores_Asignaciones.add_transition(s4,"V",s9)

# Transiciones para s5
DFA_Comparadores_Operadores_Asignaciones.add_transition(s5,"H",s6)

# Transiciones para s6
DFA_Comparadores_Operadores_Asignaciones.add_transition(s6,"Z",s7)

# Transiciones para s7
DFA_Comparadores_Operadores_Asignaciones.add_transition(s7,"C",s8)

# Transiciones para s10
DFA_Comparadores_Operadores_Asignaciones.add_transition(s10,"O",s11)
DFA_Comparadores_Operadores_Asignaciones.add_transition(s10,"R",s11)

# Transiciones para s11
DFA_Comparadores_Operadores_Asignaciones.add_transition(s11,"V",s12)
DFA_Comparadores_Operadores_Asignaciones.add_transition(s11,"C",s12)

# Verificamos si una cadena es aceptada por el DFA_Comparadores_Operadores_Asignaciones
def Validar_Comparador_Operador_Clasificacion(Cadena_Aux):
    return DFA_Comparadores_Operadores_Asignaciones.accepts(Cadena_Aux)

# <--------------------AUTÓMATA PARA COMENTARIOS VL/UL -------------------->

# Creamos el DFA_Comentarios
DFA_Comentarios = DeterministicFiniteAutomaton()

# Añadimos las transiciones al DFA_Comentarios

# Añadimos el estado inicial y los estados finales al DFA_Comentarios
DFA_Comentarios.add_start_state(t0)
DFA_Comentarios.add_final_state(t2)
DFA_Comentarios.add_final_state(t3)

# Transiciones para t0
DFA_Comentarios.add_transition(t0,"I",t1)
DFA_Comentarios.add_transition(t0,"U",t3)
for Caracter in Clasificaciones_Comentarios_UL:
    DFA_Comentarios.add_transition(t0,Caracter,t0)

# Transiciones para t1
DFA_Comentarios.add_transition(t1,"E",t1)
DFA_Comentarios.add_transition(t1,"F",t2)

# Transiciones para t3
DFA_Comentarios.add_transition(t3,"L",t3)

# Verificamos si una cadena es aceptada por el DFA_Comentarios
def Validar_Comentarios_VL_UL(Cadena_Aux):
    return DFA_Comentarios.accepts(Cadena_Aux)

# <--------------------SE EMPIEZA A LEER EL ARCHIVO Y SE SEPARA POR TOKENS CADA LINEA DE ESTE-------------------->

with open("EjemploPracticaAnalizador.java","r") as Archivo:
    Contenido_Del_Archivo = Archivo.read()
    Lineas_Del_Archivo = Contenido_Del_Archivo.split("\n") # Guarda cada linea en la lista "Lineas_Del_Archivo" pero quitando los saltos de linea

Tokens_Del_Archivo = [] # Lista donde se guardan los tokens de cada una de las lineas del archivo
Lineas = "" # Cadena donde se concatena cada una de las lineas del archivo

# Separa cada linea de "Lineas_Del_Archivo" por el espacio y las guarda en la lista "Tokens_Del_Archivo" (aquí ya es más facil analizar cada linea por separado) 
for Linea in Lineas_Del_Archivo:
    Lineas = Linea
    Tokens_Del_Archivo.append(Lineas.split(" "))
    Lineas = ""

print(f"Los tokesn del archivo son: {Tokens_Del_Archivo}")

# <--------------------NOMENCLATURA PARA CADA TOKEN DEL ARCHIVO-------------------->

# Constante Numérica = C
# Cosntante Numérica Incorrecta = M
# Variable = V
# Variable Incorrecta = W
# Palabra Reservada = P
# Operadores = O
# Comparadores = R
# Signos Ignorados = S 
# Signo de Asignación = A
# Incio de Comentarios de Varias Lineas = I
# Comentarios de Varias Lineas = E
# Final de Comentarios de Varias Lineas = F
# Incio de Comentarios de una Linea = U
# Comentarios de una Linea = L
# Paréntesis de Apertura = Y
# Paréntesis de Cierre = Z
# Palabra Reservada para Constantes Numéricas = H

# <--------------------SE CLASIFICA CADA UNO DE LOS TOKENS ASIGNANDOLES UNA LETRA-------------------->

Tokens_De_La_Linea = [] # Lista auxiliar donde se guardan los tokens de una linea
Clasificaciones = [] # Lista donde se clasifica a los tokens de todas las lineas
Clasificaciones_Por_Linea = [] # Lista donde se clasifican a los tokens de una linea

Lineas_Con_Errores = [] # Lista donde se guardan las lineas que tienen algún error
Llave = 0 # Variable para los comentarios de vl

for Numero_Linea in range(0,len(Tokens_Del_Archivo)):
    print(f"Tokens de la linea {Numero_Linea + 1}")
    print("")
    Tokens_De_La_Linea = list(Tokens_Del_Archivo[Numero_Linea])
    for Token in Tokens_De_La_Linea:
        if Token == '/*': # Si el token inicia un comentario de vl
            Llave = 1
            Clasificaciones_Por_Linea.append('I')
            print(f"El token [{Token}] es el inicio de un comentario de vl")
        elif Token == '*/': # Si el token termina un comentario de vl
            Llave = 0
            Clasificaciones_Por_Linea.append('F')
            print(f"El token [{Token}] es el final de un comentario de vl")
        else:
            if Llave == 1: # Si el token es parte del comentario de vl
                Clasificaciones_Por_Linea.append('E')
                print(f"El token [{Token}] es parte de un comentario de vl")
            else:
                if Token.isalpha() == True and Token in Palabras_Reservadas_Java: # Si el token es una palabra reservada
                    if Token in Palabras_Reservadas_Java_VN: # Si el token es una palabra reservada con valor numérico
                        Clasificaciones_Por_Linea.append('H')
                        print(f"El token [{Token}] es una palabra reservada para valor numérico")
                    else: # Si el token es una palabra reservada pero no con valor numérico 
                        Clasificaciones_Por_Linea.append('P')
                        print(f"El token [{Token}] es una palabra reservada")
                else: # Si el token no es una palabra reservada
                    if Token.startswith(('0','1','2','3','4','5','6','7','8','9','+','-')): # Si el token es un número
                        if Validar_Constante_Numerica(Token) == True: # Si el token es una constante numérica
                            Clasificaciones_Por_Linea.append('C')
                            print(f"El token [{Token}] es una constante numérica")
                        else: # Si el token no es una constante numérica
                            if Token == '+' or Token == '-': # Si el token es un operador
                                Clasificaciones_Por_Linea.append('O')
                                print(f"El token [{Token}] es un operador")
                            elif Token == '+=' or Token == '-=' or Token == '++' or Token == '--': # Si el token es un operador ignorado
                                Clasificaciones_Por_Linea.append('S')
                                print(f"El token [{Token}] se ignora")
                            else: # Si el token es una constante numérica y esta mal
                                Clasificaciones_Por_Linea.append('M')
                                print(f"El token [{Token}] es una constante numérica incorrecta")
                    else:
                        if Validar_Variables(Token) == True: # Si el token es una variable
                            Clasificaciones_Por_Linea.append('V')
                            print(f"El token [{Token}] es una variable")
                        else: # Si el token no es una variable
                            if Token == '/' or Token == '*' or Token == '%': # Si el token es un operador
                                Clasificaciones_Por_Linea.append('O')
                                print(f"El token [{Token}] es un operador")
                            elif Token == '<' or Token == '>' or Token == '<=' or Token == '>=' or Token =='!=': # Si el token es un comparador
                                Clasificaciones_Por_Linea.append('R')
                                print(f"El token [{Token}] es un comparador")
                            elif Token == '=': # Si el token es un signo de asignación
                                Clasificaciones_Por_Linea.append('A')
                                print(f"El token [{Token}] es una asignación")
                            elif Token == '//': # Si el token incia un comentario de ul
                                Clasificaciones_Por_Linea.append('U')
                                print(f"El token [{Token}] es el incio de un comentario de ul")
                            elif Token == '(': # Si el token es un paréntesis de apertura
                                Clasificaciones_Por_Linea.append('Y')
                                print(f"El token [{Token}] es un peréntesis de apertura")
                            elif Token == ')': # Si el token es un paréntesis de cierre
                                Clasificaciones_Por_Linea.append('Z')
                                print(f"El token [{Token}] es un paréntesis de cierre")
                            else: # Si el token es un signo que se ignora o una variable incorrecta
                                if (Token in Signos_Ignorados) == True or Token == 'System.out.println':
                                    Clasificaciones_Por_Linea.append('S')
                                    print(f"El token [{Token}] se ignora")
                                else:
                                    if Validar_Variables(Token) == False: # Si el token es una variable incorrecta 
                                        Clasificaciones_Por_Linea.append('W')
                                        print(f"El token [{Token}] es una variable incorrecta")

    Clasificaciones.append(Clasificaciones_Por_Linea) # Agregamos las clasificaciones de los tokens de cada linea a la lista "Clasificaciones", que contiene los de todas las lineas
    Clasificaciones_Por_Linea = []
    print("")

# <--------------------VALIDAMOS LOS COMENTARIOS UL-------------------->

Lista_Aux = [] # Lista auxiliar para guardar los tokens de cada lineas
Cadena_Aux = "" # Cadena auxiliar para concatenar y para mandar a validar

for Numero_Linea in range(0,len(Clasificaciones)): # Numero_Linea es el número de linea
    Lista_Aux = Clasificaciones[Numero_Linea]
    if ('U' in Lista_Aux) == True: # Se busca el inicio de los comentarios
        for Posicion_Token in range(Lista_Aux.index('U') + 1,len(Lista_Aux)): # Se remplazan los caracteres siguientes por comentarios
            Lista_Aux[Posicion_Token] = 'L'
        Clasificaciones[Numero_Linea] = Lista_Aux # Se sustituye la linea nueva
        for Token in Lista_Aux:
            Cadena_Aux = Cadena_Aux + Token

        # Se validan los comentarios
        if Validar_Comentarios_VL_UL(Cadena_Aux) == False:
            if ((Numero_Linea + 1) in Lineas_Con_Errores) == False:
                Lineas_Con_Errores.append(Numero_Linea + 1) # Se agrega el número de la linea con el error
    Cadena_Aux = "" # Se limpia la cadena a validar por si se tiene que validar varias veces

print(f"Las clasificaciones para cada token son: {Clasificaciones}")
print("")

# <--------------------VALIDAMOS LOS COMPARADORES/OPERADORES/ASIGNACIONES-------------------->

Lista_Aux = [] # Lista auxiliar para guardar los tokens de cada linea 
Cadena_Aux = "" # Cadena auxiliar para concatenar y para mandar a validar

for Numero_Linea in range(0,len(Clasificaciones)): # Numero_Linea es el número de linea
    Lista_Aux = Clasificaciones[Numero_Linea]
    for Posicion_Token in range(0,len(Lista_Aux)):
        if Lista_Aux[Posicion_Token] == 'O' or Lista_Aux[Posicion_Token] == 'R':
            Cadena_Aux = Lista_Aux[Posicion_Token - 1] + Lista_Aux[Posicion_Token] + Lista_Aux[Posicion_Token + 1]
            Validar_Comparador_Operador_Clasificacion_F(Cadena_Aux,Numero_Linea,Lineas_Con_Errores)
            Cadena_Aux = "" # Se limpia la cadena a validar por si se tiene que validar varias veces
        if Lista_Aux[Posicion_Token] == 'A':
            if Lista_Aux[Posicion_Token + 1] == 'Y':
                Cadena_Aux = Lista_Aux[Posicion_Token - 1] + Lista_Aux[Posicion_Token] + Lista_Aux[Posicion_Token + 1] + Lista_Aux[Posicion_Token + 2] + Lista_Aux[Posicion_Token + 3] + Lista_Aux[Posicion_Token + 4]
                Validar_Comparador_Operador_Clasificacion_F(Cadena_Aux,Numero_Linea,Lineas_Con_Errores)
                Cadena_Aux = "" # Se limpia la cadena a validar por si se tiene que validar varias veces
            else:
                Cadena_Aux = Lista_Aux[Posicion_Token - 1] + Lista_Aux[Posicion_Token] + Lista_Aux[Posicion_Token + 1]
                Validar_Comparador_Operador_Clasificacion_F(Cadena_Aux,Numero_Linea,Lineas_Con_Errores)
                Cadena_Aux = "" # Se limpia la cadena a validar por si se tiene que validar varias veces

# <--------------------VALIDAMOS LOS COMENTARIOS VL/CONSTANTE Y VARIABLE INCORRECTA-------------------->

Lista_Comentarios = [] # Lista donde se guardan las lineas donde hay comentarios
Lista_Aux = [] # Lista auxiliar para guardar los tokens de cada linea
Cadena_Aux = "" # Cadena auxiliar para concatenar y para mandar a validar

for Numero_Linea in range(0,len(Clasificaciones)): # Numero_Linea es el número de linea
    Lista_Aux = Clasificaciones[Numero_Linea]
    for Token in Lista_Aux:
        if Token == 'I' or Token == 'E':
            Cadena_Aux = Cadena_Aux + Token
            if ((Numero_Linea + 1) in Lista_Comentarios) == False:
                Lista_Comentarios.append(Numero_Linea + 1)
        elif Token == 'F':
            Cadena_Aux = Cadena_Aux + Token
            if ((Numero_Linea + 1) in Lista_Comentarios) == False:
                Lista_Comentarios.append(Numero_Linea + 1)
            
            # Se validan los comentarios
            Validar_Comentarios_VL_UL_F(Cadena_Aux,Lista_Comentarios,Lineas_Con_Errores)
            Cadena_Aux = "" # Se limpia la cadena a validar por si se tiene que validar varias veces
        elif Token == 'M' or Token == 'W':
            if ((Numero_Linea + 1) in Lineas_Con_Errores) == False:
                Lineas_Con_Errores.append(Numero_Linea + 1) # Se agrega el número de la linea con el error
        else:
            w = 0

if Cadena_Aux != "":
    # Se validan los comentarios
    Validar_Comentarios_VL_UL_F(Cadena_Aux,Lista_Comentarios,Lineas_Con_Errores)
    Cadena_Aux = "" # Se limpia la cadena a validar por si se tiene que validar varias veces
            
Lineas_Con_Errores.sort() # Se ordenan las lineas con errores

# Se imprimen las lineas que tienen Lineas_Con_Errores
if len(Lineas_Con_Errores) != 0:
    for Numero_Linea in Lineas_Con_Errores:
        print(f"Error en la línea {Numero_Linea}")
else:
    print("No hay Lineas_Con_Errores de análisis léxico en el archivo")
    print("EjemploPracticaAnalizador.java")

# <--------------------LIBERAMOS MEMORIA-------------------->

Lineas_Del_Archivo = []
Tokens_Del_Archivo = []
Lineas = ""

Tokens_De_La_Linea = []
Clasificaciones = []
Clasificaciones_Por_Linea = []

Lineas_Con_Errores = []

Lista_Aux = []
Cadena_Aux = ""