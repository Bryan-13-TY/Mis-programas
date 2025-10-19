def Automata_Pila(Cadena,Estado,Pila):
    for Letra in Cadena:
        if Estado == 'e0':
            if Letra == 'a' and Pila[-1] == 'Z0':
                Pila.append('X')
                Estado = 'e0'
                print(f"Transicion 1: Caracter: {Letra}, Pila: {Pila}, Estado: {Estado}")
            elif Letra == 'b' and Pila[-1] == 'Z0':
                Pila.append('Y')
                Estado = 'e0'
                print(f"Transicion 1: Caracter: {Letra}, Pila: {Pila}, Estado: {Estado}")
            elif Letra == 'a' and Pila[-1] == 'X':
                Pila.append('X')
                Estado = 'e0'
                print(f"Transicion 3: Caracter: {Letra}, Pila: {Pila}, Estado: {Estado}")
            elif Letra == 'b' and Pila[-1] == 'Y':
                Pila.append('Y')
                Estado = 'e0'
                print(f"Transicion 4: Caracter: {Letra}, Pila: {Pila}, Estado: {Estado}")
            elif Letra == 'a' and Pila[-1] == 'Y':
                Pila.append('X')
                Estado = 'e0'
                print(f"Transicion 5: Caracter: {Letra}, Pila: {Pila}, Estado: {Estado}")
            elif Letra == 'b' and Pila[-1] == 'X':
                Pila.append('Y')
                Estado = 'e0'
                print(f"Transicion 6: Caracter: {Letra}, Pila: {Pila}, Estado: {Estado}")
            elif Letra == 'c' and Pila[-1] == 'Z0':
                Estado = 'e1'
                print(f"Transicion 7: Caracter: {Letra}, Pila: {Pila}, Estado: {Estado}")
            elif Letra == 'c' and Pila[-1] == 'X':
                Estado = 'e1'
                print(f"Transicion 8: Caracter: {Letra}, Pila: {Pila}, Estado: {Estado}")
            elif Letra == 'c' and Pila[-1] == 'Y':
                Estado = 'e1'
                print(f"Transicion 9: Caracter: {Letra}, Pila: {Pila}, Estado: {Estado}")
            else:
                return f"La cadena {Cadena.replace('λ',"")} no es válida",Estado,Pila
        elif Estado == 'e1':
            if Letra == 'a' and Pila[-1] == 'X':
                del Pila[-1]
                Estado = 'e1'
                print(f"Transicion 10: Caracter: {Letra}, Pila: {Pila}, Estado: {Estado}")
            elif Letra == 'b' and Pila[-1] == 'Y':
                del Pila[-1]
                Estado = 'e1'
                print(f"Transicion 11: Caracter: {Letra}, Pila: {Pila}, Estado: {Estado}")
            elif Letra == 'λ' and Pila[-1] == 'Z0':
                del Pila[-1]
                Estado = 'e2'
                print(f"Transicion 12: Caracter: {Letra}, Pila: {Pila}, Estado: {Estado}")
            else:
                return f"La cadena {Cadena.replace('λ',"")} no es válida",Estado,Pila
        else:
         w = 0
    return "",Estado,int(len(Pila))

Cadena = input("Ingresa una palabra: ")
Estado = 'e0'
Pila = ['Z0']
Cadena = Cadena + 'λ'

Ms,Estado,Pila = Automata_Pila(Cadena,Estado,Pila)
if Ms != "":
    print(Ms)
else:
    if Estado == 'e2' or Pila == 0:
        print(f"La cadena {Cadena.replace('λ',"")} es válida")
    elif Estado != 'e2' or Pila != 0:
        print(f"La cadena {Cadena.replace('λ',"")} no es válida") 