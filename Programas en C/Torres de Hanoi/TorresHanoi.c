/**
 * @file TorresHanoi.c
 * @brief Resulve el problema de las torres de Hanoi.
 * 
 * Este archivo contiene la función rescursiva para resolver las torres de Hanoi.
 * 
 * @note No se ha compilado la última versión de este código. Solo funciona en Windows.
 * 
 * @author García Escamilla Bryan Alexis
 * @date 2025-10-21
 */

#include <stdio.h>
#include <stdlib.h>
#include <conio.h>

#define VERSION "1.2"

void Hanoi(int num_disks, int *num_movements, char origin, char auxiliar, char destiny);

// Programa principal
int main(int argc, char const *argv[]) {
    int num_disks, op = 0, num_movements = 0;
    char origin = 'A', auxiliar = 'B', destiny = 'C';

    do {
        system("cls");
        printf("/*----------------.");
        printf("\n| TORRES DE HANOI |");
        printf("\n`----------------*/");
        printf("\n\n1.- Resolver las torres de hanoi");
        printf("\n2.- Salir del programa");
        printf("\n\nOpcion: ");
        scanf("%d", &op);

        switch (op) {
            case 1:
                printf("\n__RESOLVER TORRES DE HANOI__");
                printf("\n\nCuantos discos quiere resolver? ");
                scanf("%d", &num_disks);
                printf("\nMovimientos para %d discos:\n", num_disks);
                Hanoi(num_disks, &num_movements, origin, auxiliar, destiny);
                num_movements = 0;
                getch();
                break;
            case 2:
                printf("\nGracias por probar el programa, vuelva pronto");
                getch();
                break;
            default:
                printf("\nLa opcion no es valida");
                getch();
                break;
        }
    } while (op != 2);

    return 0;
}

/**
 * @brief Resuelve recursivamente las torres de Hanoi.
 * 
 * Esta función resuelve recursivamente el problema de las torres de Hanoi imprimiendo los
 * movimientos correspondientes para ello.
 * 
 * @param num_disks Número de discos a resolver.
 * @param num_movements Puntero al número de movimientos.
 * @param origin Torre de origen.
 * @param auxiliar Torre auxiliar.
 * @param destiny Torre de destino.
 */
void Hanoi(int num_disks, int *num_movements, char origin, char auxiliar, char destiny) {
    if (num_disks == 1) {
        (*num_movements)++;
        printf("\nMovimiento %d: Mover el disco desde %c hasta %c", *num_movements, origin, destiny);
    } else {
        Hanoi(num_disks - 1, num_movements, origin, destiny, auxiliar);
        (*num_movements)++;
        printf("\nMovimiento %d: Mover el disco desde %c hasta %c", *num_movements, origin, destiny);
        Hanoi(num_disks - 1, num_movements, auxiliar, origin, destiny);
    }
}