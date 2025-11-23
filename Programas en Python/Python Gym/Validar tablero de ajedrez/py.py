def isValidChessBoard(board: dict) -> bool:
    Llaves = board.keys()
    Valores = board.values()

    for i, key in enumerate(Llaves):
        print(f"{i}. {key}")

    lista = [[0 for _ in range(8)] for _ in range(8)]
    print(lista)

    for i in range(len(lista)):
        print(lista[i])

    matrix = {'1a': "", '2a': "", '3a': "", '4a': "", '5a': "", '6a': "", '7a': "", '8a': "",
              '1a': "", '2a': "", '3a': "", '4a': "", '5a': "", '6a': "", '7a': "", '8a': "",
              '1a': "", '2a': "", '3a': "", '4a': "", '5a': "", '6a': "", '7a': "", '8a': "",
              '1a': "", '2a': "", '3a': "", '4a': "", '5a': "", '6a': "", '7a': "", '8a': "",
              '1a': "", '2a': "", '3a': "", '4a': "", '5a': "", '6a': "", '7a': "", '8a': "",
              '1a': "", '2a': "", '3a': "", '4a': "", '5a': "", '6a': "", '7a': "", '8a': "",
              '1a': "", '2a': "", '3a': "", '4a': "", '5a': "", '6a': "", '7a': "", '8a': "",
              '1a': "", '2a': "", '3a': "", '4a': "", '5a': "", '6a': "", '7a': "", '8a': "",}


board = {'1h': 'bking', '6c': 'wqueen', '2g': 'bbishop', '5h': 'bqueen', '3e': 'wking'}
isValidChessBoard(board)