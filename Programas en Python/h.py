cadena = "variable=3*(10/(100+100))"
lista = []
aux = ""

for c in cadena:
    print(aux)
    if (c == " "):
        if (not aux == ""):
            lista.append(aux)
            aux = ""
        else:
            continue
    else:
        if (c.isalpha()):
            aux = aux + c

        if (c.isnumeric()):
            aux = aux + c

        if (c == '(' or c == ')'):
            if (not aux == ""):
                lista.append(aux)
                aux = c
                lista.append(c)
            else:
                aux = aux + c
                lista.append(aux)
        elif (c == '='):
            if (not aux == ""):
                lista.append(aux)
                aux = c
                lista.append(c)
            else:
                aux = aux + c
                lista.append(aux)
        elif (c == '+' or c == '-' or c == '*' or c == '/'):
            if (not aux == ""):
                lista.append(aux)
                aux = c
                lista.append(c)
            else:
                aux = aux + c
                lista.append(aux)

print(f"{lista}")

c = '('
aux = ""
lista = ['variable', '=', '3', '*'] 