#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <stdbool.h>
#include <time.h>

#define NOOB_MINES 10
#define AMATEUR_MINES 40
#define EXPERIENCED_MINES 99

void inicializarTablero(int height, int width, char board[height][width], int numMines);
void agregarMinas(int *height, int *width, char board[*height][*width], int *numMines);
void contarMinas(int *height, int *width, char board[*height][*width]);

int main(int argc, char const *argv[]) {

    //bool Estado = true;

    ///printf("Estado: %d", !Estado);
    int op, height = 0, width = 0, numMines = 0;

    do {
        system("cls");
        printf("/*------------------.");
        printf("\n| BUSCAMINAS BASICO |");
        printf("\n`------------------*/");
        printf("\n\n>> Elije una dificultad");
        printf("\n\n1.- Novato (10 minas)");
        printf("\n2.- Aficionado (40 minas)");
        printf("\n3.- Experimentado (99 minas)");
        printf("\n4.- Salir del programa");
        printf("\n\nOpcion: ");
        scanf("%d", &op);

        switch (op) {
            case 1:
                printf("\n/*-------------------.");
                printf("\n| DIFICULTAD: NOVATO |");
                printf("\n`-------------------*/");
                printf("\n\nMinas por buscar: %d", NOOB_MINES);
                printf("\nDimensiones del tablero: 9 x 9\n\n");
                height = 9; width = 9; numMines = NOOB_MINES;
                break;
            case 2:
                printf("\n/*-----------------------.");
                printf("\n| DIFICULTAD: AFICIONADO |");
                printf("\n`-----------------------*/");
                printf("\n\nMinas por buscar: %d", AMATEUR_MINES);
                printf("\nDimensiones del tablero: 16 x 16\n\n");
                height = 16; width = 16; numMines = AMATEUR_MINES;
                break;
            case 3:
                printf("\n/*--------------------------.");
                printf("\n| DIFICULTAD: EXPERIMENTADO |");
                printf("\n`--------------------------*/");
                printf("\n\nMinas por buscar: %d", EXPERIENCED_MINES);
                printf("\nDimnesiones del tablero: 16 x 30\n\n");
                height = 16; width = 30; numMines = EXPERIENCED_MINES;
                break;
            case 4:
                printf("\nGracias por probar el programa, vuelva pronto");
                getch();
                break;
            default:
                printf("\n>> ERROR: Opcion no valida");
                getch();
                break;
        }

        if (op == 1 || op == 2 || op == 3) { // Para que solo se haga con los valores de op correctos
            char board[height][width];
            inicializarTablero(height, width, board, numMines);
            getch();
        }
    } while (op != 4);
    return 0;
}

void inicializarTablero(int height, int width, char board[height][width], int numMines) {
    // Se inicializa el tablero con ceros
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            board[i][j] = 0;
        }
    }

    agregarMinas(&height, &width, board, &numMines);
    contarMinas(&height, &width, board);

    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            printf(" %d ", board[i][j]);
        }
        printf("\n");
    }
}

void agregarMinas(int *height, int *width, char board[*height][*width], int *numMines) {
    int mines = 0; srand(time(NULL));

    while (mines < (*numMines)) {
        int row = 0 + rand() % ((*height - 1) - 0 + 1);
        int colum = 0 + rand() % ((*width - 1) - 0 + 1);

        if (board[row][colum] == 0) {
            board[row][colum] = -1;
            mines++;
        }
    }
}

void contarMinas(int *height, int *width, char board[*height][*width]) {
    for (int i = 0; i < (*height); i++) {
        for (int j = 0; j < (*width); j++) {
            if (board[i][j] == -1) { // Si hay una mina en la celda
                continue;
            }

            int count = 0; // Contador de minas vecinas

            // Recorremos el vecindario de 3x3
            for (int di = -1; di <= 1; di++) {
                for (int dj = -1; dj <= 1; dj++) {
                    if (di == 0 && dj == 0) { // Si no hay minas alrededor
                        continue;
                    }

                    int ni = i + di;
                    int nj = j + dj;

                    // Verificamos que esté dentro de los límites
                    if (ni >= 0 && ni < (*height) && nj >= 0 && nj < (*width)) {
                        if (board[ni][nj] == -1) { // Si hay una mina
                            count++;
                        }
                    }
                }
            }

            board[i][j] = count;
        }
    }
}