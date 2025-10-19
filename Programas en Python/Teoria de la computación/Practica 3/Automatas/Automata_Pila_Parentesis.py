def Automata_Pila_Parentesis(Cadena,Estado,Pila):
    for Letra in Cadena:    
        if Estado == 'e0':
            if Letra == '(' and Pila[-1] == 'z0':
                Pila.append('Pa')
                Estado = 'e0'
                print(f"Transicion 1: Caracter: {Letra}, Pila: {Pila}, Estado: {Estado}")
            elif Letra == '(' and Pila[-1] == 'Pa':
                Pila.append('Pa')
                Estado = 'e0'
                print(f"Transicion 2: Caracter: {Letra}, Pila: {Pila}, Estado: {Estado}")
            elif Letra == ')' and Pila[-1] == 'Pa':
                del Pila[-1]
                Estado = "e0"
                print(f"Transicion 3: Caracter: {Letra}, Pila: {Pila}, Estado: {Estado}")
            elif Letra == ';' and Pila[-1] == 'z0':
                del Pila[-1]
                Estado = 'e1'
                print(f"Transicion 4: Caracter: {Letra}, Pila: {Pila}, Estado: {Estado}")
            else:
                return f"La cadena {Cadena.replace('λ',"")} no pertenece a la gramática",Estado,Pila
        else:
            w = 0
    return "",Estado,int(len(Pila))

Cadena = input("Ingresa una cadena: ")
Estado = 'e0'
Pila = ['z0']
Cadena = Cadena + 'λ'

Mensaje,Estado,Pila = Automata_Pila_Parentesis(Cadena,Estado,Pila)
if Mensaje != "":
    print(Mensaje)
else:
    if Estado == 'e1' or Pila == 0:
        print(f"La cadena {Cadena.replace('λ',"")} pertenece a la gramática")
    elif Estado != 'e1' or Pila != 0:
        print(f"La cadena {Cadena.replace('λ',"")} no pertenece a la gramática") 