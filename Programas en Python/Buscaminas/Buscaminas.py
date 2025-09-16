from Funciones import menu

print("""
/*------------------.
| BUSCAMINAS BÁSICO |
`------------------*/
      
>> Elije la dificultad

1.- Novato (10 minas)
2.- Aficionado (40 minas)
3.- Experimentado (99 minas)
""")

difficult = input("Opción: ")
menu(difficult)