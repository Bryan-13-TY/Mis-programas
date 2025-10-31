def compresion_de_listas() -> tuple[list[int], list[int]]:
    cuadrados_normal = []

    # Forma normal
    for i in range(10):
        cuadrados_normal.append(i**2)

    # Forma elegante
    cuadrados_elegante = [i**2 for i in range(10)]

    return cuadrados_normal, cuadrados_elegante

def intercambiar_variables():
    x = 3
    y = 2
    z = 5

    print(f"Antes del intercambio {x=}, {y=}, {z=}")

    x, y, z = y, z, x # Asignación de derecha a inzquierda

    print(f"Después del intercambio {x=}, {y=}, {z=}")

def enumerar():
    lista = [i**2 for i in range(20)]

    for i, valor in enumerate(lista):
        print(f"Número {i + 1}: {valor}")

def recorrer_listas():
    nombres = ["Bryan", "Carlos", "Ricardo", "Ximena", "Frida", "Luis", "Rodrigo"]
    calificaciones = [7.8, 9.5, 10, 5.2, 2, 6.7, 7.9]

    for nombre, calificacion in zip(nombres, calificaciones):
        print(f"La calificación de {nombre} es {calificacion}")

def main():
    print("""
Trucos en python
""")
    
    recorrer_listas()

if (__name__ == "__main__"):
    main()