import numpy as np

def revelarCelda(row: int, colum: int, height: int, width: int, board, visible) -> None:
    if not (0 <= row < height and 0 <= colum < width):
        return
    if visible[row][colum]:
        return # Ya esta revelada
    
    visible[row][colum] = True

    if (board[row][colum] == 0):
        # Expandir a los vecinos si es cero
        for drow in [-1, 0, 1]:
            for dcolum in [- 1, 0, 1]:
                if (drow == 0 and dcolum == 0):
                    continue
                
                revelarCelda(row + drow, colum + dcolum, height, width, board, visible)

def imprimirTablero(height: int, width: int, board, visible, flags, reveal_all = False) -> None:
    for row in range(height):
        line = ""

        for colum in range(width):
            if (not reveal_all and flags[row][colum]):
                line += " F " # Bandera
            elif (not reveal_all and not visible[row][colum]):
                line += " # " # Celda oculta
            else:
                if (board[row][colum] == -1):
                    line += " * " # Mina
                elif (board[row][colum] == 0):
                    line += " . " # Vacío
                else:
                    line += f" {board[row][colum]} " 
        
        print(line)
    print()

def inicializarTablero(height: int, width: int, numMines: int) -> None:
    board = np.zeros((height, width), dtype = int) # Se inicializa un talero vacio (puros ceros)

    # Se llena el tablero con numMines minas aleatorias
    i = 0
    
    while (i < numMines):
        row = np.random.randint(0, height)
        colum = np.random.randint(0, width)

        if (board[row][colum] == 0): # Si la celda está vacía
            board[row][colum] = -1 # Se coloca una mina en esa celda

            i += 1

    # Se calculan las minas alrededor de la mina
    for row in range(height):
        for colum in range(width):
            if (board[row][colum] == -1): # Hay una mina en la celda
                continue

            # Se cuentas la minas vecinas
            count = 0

            for drow in [- 1, 0, 1]:
                for dcolum in [- 1, 0, 1]:
                    if (drow == 0 and dcolum == 0): # Si no hay minas alrededor
                        continue
                    
                    nrow, ncolum = row + drow, colum + dcolum

                    if (0 <= nrow < height and 0 <= ncolum < width): # Si nos encontramos dentro del vecindario
                        if (board[nrow][ncolum] == -1): # Si hay una mina
                            count += 1

            board[row][colum] = count 

    return board

def menu(difficult: str) -> None:
    match (difficult.strip()):
        case '1':
            height, width, mines = 9, 9, 10
            print("""
/*-------------------.
| DIFICULTAD: NOVATO |
`-------------------*/
                  
Minas por buscar: 10
Dimensines del tablero: 9 x 9
""")
        case '2':
            height, width, mines = 16, 16, 40
            print("""
/*-----------------------.
| DIFICULTAD: AFICIONADO |
`-----------------------*/

Minas por buscar: 40
Dimensiones del tablero: 16 x 16
""")
        case '3':
            height, width, mines = 16, 30, 99
            print("""
/*--------------------------.
| DIFICULTAD: EXPERIMENTADO |
`--------------------------*/
        
Minas por buscar: 100
Dimensiones del tablero: 16 x 30
""")
        case _:
            print(">> Opción no válida")
            return
        
    board = inicializarTablero(height, width, mines)
    visible = np.full((height, width), False, dtype = bool)
    flags = np.full((height, width), False, dtype = bool)

    print("Tablero oculto:\n")
    imprimirTablero(height, width, board, visible, flags)

    while True:
        print("Elije acción: (r fila columa = revelar, f fila columna = bandera)")
        action = input(">>> ").strip().split()

        if (len(action) != 3):
            print(">> Entrada inválida")
            continue
    
        cmd, rows, cols = action

        try:
            row, colum = int(rows), int(cols)

            if not (0 <= row < height and 0 <= colum < width):
                print(">> Celda fuera del tablero.")
                continue
        except:
            print(">> Entrada invalida")
            continue

        if (cmd.lower() == 'r'):
            if (flags[row][colum]):
                print(">> Hay una bandera en esa celda, quitala primero.")
                continue

            revelarCelda(row, colum, height, width, board, visible)

            if (board[row][colum] == -1):
                print("¡BOOM! ¡Has pisado una mina! 💥")
                imprimirTablero(height, width, board, visible, flags, reveal_all = True)
                break
        elif (cmd.lower() == 'f'):
            flags[row][colum] = not flags[row][colum] # Alterna bandera
        else:
            print(">> Comando no válido, usa 'r' paar revelar o 'f' para bandera")
            continue

        imprimirTablero(height, width, board, visible, flags)

        if (board[row][colum] == -1):
            print("¡BOOM! ¡Has pisado una mina! 💥")
            imprimirTablero(height, width, board, visible, flags, reveal_all = True)
            break

        # Comprobar si gano
        if (np.all((board != -1) | visible)):
            print("¡Felicidades ¡Has ganado! 🎉")
            imprimirTablero(height, width, board, visible, flags, reveal_all = True)
            break
