#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX 16
#define MAX2 16
#define MINES 40

void imprimirTablero(char board[MAX][MAX2]) {
    for (int i = 0; i < MAX; i++) {
        for (int j = 0; j < MAX2; j++) {
            printf(" %d ", board[i][j]);
        }
        printf("\n");
    }
}

int main(int argc, char const *argv[]) {
    int count = 0, i = 0;
    char board[MAX][MAX2] = {0};
    
    srand(time(NULL)); // Inicializar semilla

    printf("Tablero sin minas: \n\n");
    imprimirTablero(board);

    while (count < MINES) {
        int row = 0 + rand() % ((MAX - 1) - 0 + 1);
        int colum = 0 + rand() % ((MAX2 - 1) - 0 + 1);

        if (board[row][colum] == 0) {
            board[row][colum] = -1;
            count++;
        }

        i++;
        //printf("Posición de la mina %d: [%d, %d]\n", count + 1, row, colum);
    }

    printf("\nTablero con %d minas (%d iteraciones): \n\n", count, i);
    imprimirTablero(board);

    return 0;
}