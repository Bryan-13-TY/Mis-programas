import nltk
from nltk import CFG

# Definir la gramática
Gramatica = CFG.fromstring("""
  S -> E ';'
  E -> A | R
  A -> 'v' '=' R
  R -> T | R '+' T | R '-' T
  T -> F | T '*' F | T '/' F | T '%' F
  F -> 'v' | 'c' | '(' R ')'
""")

# Crear el parser
Parser = nltk.ChartParser(Gramatica)

# Analizar una oración
Cadena_Aux = "v = ( c + ( ( v + v ) * c ) ) * ( v - v ) ;"

# Tokenizar la oración
Tokens = nltk.word_tokenize(Cadena_Aux)
print("Tokens:", Tokens)  # Imprimir los tokens para verificar

# Intentar parsear y mostrar los árboles de análisis
try:
    found_parse = False
    for tree in Parser.parse(Tokens):
        found_parse = True
        print("Árbol de análisis sintáctico:")
        tree.pretty_print()
    
    if not found_parse:
        print("No se encontraron árboles de análisis sintáctico válidos.")

except ValueError as error:
    print(f"No se puede analizar la oración: {error}")