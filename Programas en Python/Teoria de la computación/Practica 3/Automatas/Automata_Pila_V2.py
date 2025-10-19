def Automata_Pila(Palabra,Estado,Pila1,Pila2):
    print("Proceso de validación de la palabra: ")
    print("")
    for Letra in Palabra:
        if Estado == 'q0':
            if Letra == 'V' and Pila1[-1] == 'z0':
                Pila1.append('V')
                Estado = 'q1'
                print(f"Transicion 1: Caracter: {Letra}, Pila1: {Pila1}, Pila2: {Pila2} Estado: {Estado}")
            else:
                return f"La palabra {Palabra} no pertenece a la gramática",Estado,Pila1,Pila2
        elif Estado == 'q1':
            if Letra == 'A' and Pila1[-1] == 'V':
                Pila1.append('A')
                Estado = 'q2'
                print(f"Transicion 2: Caracter: {Letra}, Pila1: {Pila1}, Pila2: {Pila2} Estado: {Estado}")
            else:
                return f"La palabra {Palabra} no pertenece a la gramática",Estado,Pila1,Pila2
        elif Estado == 'q2':
            if Letra == 'V' and Pila1[-1] == 'A':
                Pila1.append('V')
                Estado = 'q2'
                print(f"Transicion 3: Caracter: {Letra}, Pila1: {Pila1}, Pila2: {Pila2} Estado: {Estado}")
            elif Letra == 'C' and Pila1[-1] == 'A':
                Pila1.append('C')
                Estado = 'q2'
                print(f"Transicion 4: Caracter: {Letra}, Pila1: {Pila1}, Pila2: {Pila2} Estado: {Estado}")
            elif Letra == 'Y' and Pila2[-1] == 'z0':
                Pila2.append('Pa')
                Estado = 'q2'
                print(f"Transicion 5: Caracter: {Letra}, Pila1: {Pila1}, Pila2: {Pila2} Estado: {Estado}")
            elif Letra == 'Z' and Pila2[-1] == 'Pa':
                del Pila2[-1]
                Estado = 'q2'
                print(f"Transicion 6: Caracter: {Letra}, Pila1: {Pila1}, Pila2: {Pila2} Estado: {Estado}")
            elif Letra == 'Y' and Pila2[-1] == 'Pa':
                Pila2.append('Pa')
                Estado = 'q2'
                print(f"Transicion 7: Caracter: {Letra}, Pila1: {Pila1}, Pila2: {Pila2} Estado: {Estado}")
            elif Letra == 'A' and Pila1[-1] == 'V':
                Pila1.append('A')
                Estado = 'q2'
                print(f"Transicion 8: Caracter: {Letra}, Pila1: {Pila1}, Pila2: {Pila2} Estado: {Estado}")
            elif Letra == 'O' and Pila1[-1] == 'V':
                Pila1.append('O')
                Estado = 'q3'
                print(f"Transicion 9: Caracter: {Letra}, Pila1: {Pila1}, Pila2: {Pila2} Estado: {Estado}")
            elif Letra == 'O' and Pila1[-1] == 'C':
                Pila1.append('O')
                Estado = 'q3'
                print(f"Transicion 10: Caracter: {Letra}, Pila1: {Pila1}, Pila2: {Pila2} Estado: {Estado}")
            elif Letra == 'X' and Pila1[-1] == 'C':
                Pila1.append('X')
                del Pila2[-1]
                Estado = 'q4'
                print(f"Transicion 11: Caracter: {Letra}, Pila1: {Pila1}, Pila2: {Pila2} Estado: {Estado}")
            elif Letra == 'X' and Pila1[-1] == 'V':
                Pila1.append('X')
                del Pila2[-1]
                Estado = 'q4'
                print(f"Transicion 12: Caracter: {Letra}, Pila1: {Pila1}, Pila2: {Pila2} Estado: {Estado}")
            else:
                return f"La palabra {Palabra} no pertenece a la gramática",Estado,Pila1,Pila2
        elif Estado == 'q3':
            if Letra == 'C' and Pila1[-1] == 'O':
                Pila1.append('C')
                Estado = 'q3'
                print(f"Transicion 13: Caracter: {Letra}, Pila1: {Pila1}, Pila2: {Pila2} Estado: {Estado}")
            elif Letra == 'V' and Pila1[-1] == 'O':
                Pila1.append('V')
                Estado = 'q3'
                print(f"Transicion 14: Caracter: {Letra}, Pila1: {Pila1}, Pila2: {Pila2} Estado: {Estado}")
            elif Letra == 'O' and Pila1[-1] == 'V':
                Pila1.append('O')
                Estado = 'q3'
                print(f"Transicion 15: Caracter: {Letra}, Pila1: {Pila1}, Pila2: {Pila2} Estado: {Estado}")
            elif Letra == 'O' and Pila1[-1] == 'C':
                Pila1.append('O')
                Estado = 'q3'
                print(f"Transicion 16: Caracter: {Letra}, Pila1: {Pila1}, Pila2: {Pila2} Estado: {Estado}")
            elif Letra == 'Y' and Pila2[-1] == 'Pa':
                Pila2.append('Pa')
                Estado == 'q3'
                print(f"Transicion 17: Caracter: {Letra}, Pila1: {Pila1}, Pila2: {Pila2} Estado: {Estado}")
            elif Letra == 'Z' and Pila2[-1] == 'Pa':
                del Pila2[-1]
                Estado = 'q3'
                print(f"Transicion 18: Caracter: {Letra}, Pila1: {Pila1}, Pila2: {Pila2} Estado: {Estado}")
            elif Letra == 'Y' and Pila2[-1] == 'z0':
                Pila2.append('Pa')
                Estado = 'q3'
                print(f"Transicion 19: Caracter: {Letra}, Pila1: {Pila1}, Pila2: {Pila2} Estado: {Estado}")
            elif Letra == 'X' and Pila1[-1] == 'C':
                Pila1.append('X')
                del Pila2[-1]
                Estado = 'q4'
                print(f"Transicion 20: Caracter: {Letra}, Pila1: {Pila1}, Pila2: {Pila2} Estado: {Estado}")
            elif Letra == 'X' and Pila1[-1] == 'V':
                Pila1.append('X')
                del Pila2[-1]
                Estado = 'q4'
                print(f"Transicion 21: Caracter: {Letra}, Pila1: {Pila1}, Pila2: {Pila2} Estado: {Estado}")
            else:
                return f"La palabra {Palabra} no pertenece a la gramática",Estado,Pila1,Pila2
        else:
            w = 0
    return "",Estado,int(len(Pila1)),int(len(Pila2))        

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

Palabra = input("Ingrese una palabra: ")
Estado = 'q0'
Pila1 = ['z0'] # Pila para validar el orden de las variables, constantes y operadores
Pila2 = ['z0'] # Pila para validar el ordden de los parentesis

Mensaje,Estado,Pila1,Pila2 = Automata_Pila(Palabra,Estado,Pila1,Pila2)

if Mensaje != "":
    print(Mensaje)
else:
    if Estado == 'q4' and Pila2 == 0:
        print("")
        print(f"La palabra {Palabra} pertenece a la gramática")
    elif Estado != 'q4' and Pila2 != 0:
        print("")
        print(f"La palabra {Palabra} no pertenece a la gramática")
    elif Estado != 'q4' or Pila2 != 0:
        print("")
        print(f"La palabra {Palabra} no pertenece a la gramática")