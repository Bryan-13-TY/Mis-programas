import nltk
from nltk import CFG

# Definir la gramática independiente del contexto (CFG)
grammar = CFG.fromstring("""
    S -> E ';'
    E -> 'v' '=' E | E '+' T | E '-' T | T
    T -> T '*' F | T '/' F | T '%' F | F
    F -> 'v' | 'c' | '(' E ')'
""")

# Crear el analizador sintáctico
parser = nltk.ChartParser(grammar)

# Oración a analizar
sentence = "v = v + c ;".split()

# Analizar la oración y generar los árboles de derivación
for tree in parser.parse(sentence):
    print(tree)
    tree.pretty_print()