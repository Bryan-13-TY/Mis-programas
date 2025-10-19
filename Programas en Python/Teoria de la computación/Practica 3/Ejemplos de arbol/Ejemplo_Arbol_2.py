import nltk
from nltk import CFG

# Definir la gramática
gramatica = CFG.fromstring("""
  S -> A ';' | ';'
  A -> A '(' A ')' | '(' ')' | '(' A ')' | A '(' ')'
""")

# Crear el parser
parser = nltk.ChartParser(gramatica)

# Analizar una oración
oracion = "((()(()))((())));"

# Tokenizar la oración
tokens = nltk.word_tokenize(oracion)
print("Tokens:", tokens)  # Imprimir los tokens para verificar

# Intentar parsear y mostrar los árboles de análisis
try:
    found_parse = False
    for tree in parser.parse(tokens):
        found_parse = True
        print("Árbol de análisis sintáctico:")
        tree.pretty_print()
    
    if not found_parse:
        print("No se encontraron árboles de análisis sintáctico válidos.")

except ValueError as e:
    print(f"No se puede analizar la oración: {e}")