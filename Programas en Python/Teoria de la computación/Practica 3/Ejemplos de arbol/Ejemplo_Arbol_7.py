import nltk
from nltk import CFG

# Definir la gramática independiente del contexto (CFG)
grammar = CFG.fromstring("""
    S -> E ';'
    E -> 'v' '=' A | 'v' '=' R | R '+' T | R '-' T | T '*' F | T '/' F | T '%' F | 'v' | 'c' | '(' R ')'
    A -> 'v' '=' A | 'v' '=' R
    R -> R '+' T | R '-' T | T '*' F | T '/' F | T '%' F | 'v' | 'c' | '(' R ')'
    T -> T '*' F | T '/' F | T '%' F | 'v' | 'c' | '(' R ')'
    F -> 'v' | 'c' | '(' R ')'
""")

# Crear el árbol de derivación
parser = nltk.ChartParser(grammar)

# Oración a analizar
sentence = "v = ( ( ( v + c ) * ( v % ( c * c * v ) ) ) + ( ( v + ( v * v ) ) / c ) ) ;".split()

# Analizar la oración y generar los árboles de derivación
try:
    fond_parse = False
    for tree in parser.parse(sentence):
        fond_parse = True
        print("Árbol de derivación:")
        print("")
        print("Elige como quiere que se muestre el árbol de derivación: MT = Texto, MG = Dibujo, AM = Ambos modos\n")
        Opcion = input("\nOpción: ")
        if Opcion == 'MT':
            tree.pretty_print()
        elif Opcion == 'MG':
            tree.draw()
        elif Opcion == 'AM':
            tree.pretty_print()
            tree.draw()
        else:
            print("Opción no válida")
    if not fond_parse:
        print("No se encontraron árboles de derivación válidos")
except ValueError as error:
    print(f"No se puede analizar la expresión: {error}")