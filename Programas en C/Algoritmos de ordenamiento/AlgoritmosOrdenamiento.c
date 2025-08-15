/**
 * @file AlgoritmosOrdenamiento.c
 * @brief Implementa los 4 algoritmos de ordenamiento.
 * 
 * Este archivo contiene los 4 algoritmos de ordenamiento: Inserción, burbuja, selección y mezcla.
 * 
 * @note No se ha compilado la última versión de este código. Solo funciona en Windows.
 * 
 * @author García Escamilla Bryan Alexis
 * @date 2025-08-14
 */

#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <time.h>

#define SIZE 30 // Tamaño del arreglo

void LLenarArreglo(int array[SIZE]);
void ImprimirArreglo(int array[SIZE]);
void Ord_Insercion(int array[SIZE]);
void Ord_Burbuja(int array[SIZE]);
void Ord_Seleccion(int array[SIZE]);
void Ord_Mezcla(int array[SIZE], int beginning, int end);
void Mezcla_Aux(int array[SIZE], int beggining, int middle, int end);

// Programa principal
int main(int argc, char const *argv[]) {
    int op = 0, size = SIZE - 1;
    int array[SIZE];

    do {
        system("cls");
        printf("/*---------------------------.");
        printf("\n| ALGORITMOS DE ORDENAMIENTO |");
        printf("\n`---------------------------*/");
        LLenarArreglo(array);
        printf("\n\nArreglo a ordenar: ");
        ImprimirArreglo(array);
        printf("\n\nElije un algoritmo:");
        printf("\n\n1.- Insercion");
        printf("\n2.- Burbuja");
        printf("\n3.- Seleccion");
        printf("\n4.- Mezcla");
        printf("\n5.- Salir del programa");
        printf("\n\nOpcion: ");
        scanf("%d", &op);

        switch (op) {
            case 1:
                printf("\n__ORDENAMIENTO POR INSERCION__");
                Ord_Insercion(array);
                printf("\n\nArreglo ordenado: ");
                ImprimirArreglo(array);
                getch();
                break;
            case 2:
                printf("\n__ORDENAMIENTO POR BURBUJA__");
                Ord_Burbuja(array);
                printf("\n\nArreglo ordenado: ");
                ImprimirArreglo(array);
                getch();
                break;
            case 3:
                printf("\n__ORDENAMIENTO POR SELECCION__");
                Ord_Seleccion(array);
                printf("\n\nArreglo ordenado: ");
                ImprimirArreglo(array);
                getch();
                break;
            case 4:
                printf("\n__ORDENAMIENTO POR MEZCLA__");
                Ord_Mezcla(array, 1, SIZE - 1);
                printf("\n\nArreglo ordenado: ");
                ImprimirArreglo(array);
                getch();
                break;
            case 5:
                printf("\nGracias por probar el programa, vuelva pronto");
                getch();
                break;
            default:
                printf("\nLa opcion no es valida");
                getch();
                break;
        }
    } while(op != 5);
    
    return 0;
}

/**
 * @brief Llena un arreglo con números aleatorios.
 * 
 * Esta función llena un arreglo de tamaño SIZE con números del 1 al 99.
 * 
 * @param array Arreglo a llenar.
 */
void LLenarArreglo(int array[SIZE]) {
    srand(time(NULL));

    for (int i = 0; i < SIZE - 1; i++) {
        int aux = rand() %99 + 1;
        array[i + 1] = aux;
    }
}

/**
 * @brief Imprime un arreglo.
 * 
 * Esta función imprime un arreglo desde la posición 1.
 * 
 * @param array Arreglo a imprimir.
 */
void ImprimirArreglo(int array[SIZE]) {
    for (int i = 0; i < SIZE - 1; i++) {
        printf("[%d]", array[i + 1]);
    }
}

/**
 * @brief Ordena un arreglo por inserción.
 * 
 * Esta función implementa el algoritmo de ordenamiento por inserción.
 * 
 * @param array Arreglo a ordenar por este algoritmo.
 */
void Ord_Insercion(int array[SIZE]) {
    for (int b = 1; b <= SIZE - 1; b++) {
        int key = array[b];
        int a = b - 1;

        while (a > 0 && array[a] > key) {
            array[a + 1] = array[a];
            a--;
        }

        array[a + 1] = key;
    }
}

/**
 * @brief Ordena un arreglo por burbuja.
 * 
 * Esta función implementa el algoritmo de ordenamiento por burbuja.
 * 
 * @param array Arreglo a ordenar por este algoritmo.
 */
void Ord_Burbuja(int array[SIZE]) {
    for (int i = 1; i < SIZE - 1; i++) {
        for (int j = 1; j < SIZE - 1; j++) {
            if (array[j] > array[j + 1]) {
                int aux = array[j];
                array[j] = array[j + 1];
                array[j + 1] = aux;
            }
        }
    }
}

/**
 * @brief Ordena un arreglo por selección.
 * 
 * Esta función implementa el algoritmo de ordenamiento por selección.
 * 
 * @param array Arreglo a ordenar por este algoritmo.
 */
void Ord_Seleccion(int array[SIZE]) {
    for (int i = 1; i <= SIZE - 1; i++) {
        int aux = array[i];
        int key = i;

        for (int j = i + 1; j <= SIZE - 1; j++) {
            if (array[j] < aux) {
                aux = array[j];
                key = j;
            }
        }

        array[key] = array[i];
        array[i] = aux;
    }
}

/**
 * @brief Ordena un arreglo por mezcla.
 * 
 * Esta función implementa el algoritmo de ordenamiento por mezcla.
 * 
 * @param array Arreglo a ordenar por este algoritmo.
 * @param beggining Posición inicial del arreglo.
 * @param end Posición final del arreglo. 
 */
void Ord_Mezcla(int array[SIZE], int beggining, int end) {
    if (beggining < end) {
        int middle = (beggining + end) / 2;

        Ord_Mezcla(array, beggining, middle);
        Ord_Mezcla(array, middle + 1, end);
        Mezcla_Aux(array, beggining, middle, end);
    }
}

/**
 * @brief Algoritmo de ordenamiento por mezcla.
 * 
 * Función en donde se implementa como tal el algoritmo de ordenamiento por mezcla.
 * 
 * @param array Arreglo a ordenar poe este algoritmo.
 * @param beggining Posición inicial del arreglo.
 * @param middle Posición media del arreglo.
 * @param end Posición final del arreglo.
 */
void Mezcla_Aux(int array[SIZE], int beggining, int middle, int end) {
    int number_1 = middle - beggining + 1;
    int number_2 = end - middle;
    int L[number_1], R[number_2];

    for (int i = 0; i < number_1; i++) {
        L[i] = array[beggining + i];
    }

    for (int i = 0; i < number_2; i++) {
        R[i] = array[middle + i + 1];
    }

    int key = beggining, i = 0, j = 0;

    while (i < number_1 && j < number_2) {
        if (L[i] <= R[j]) {
            array[key] = L[i];
            i++;
        } else {
            array[key] = R[j];
            j++;
        }
        key++;
    }

    while (i < number_1) {
        array[key] = L[i];
        i++;
        key++;
    }

    while (j < number_2) {
        array[key] = R[j];
        j++;
        key++;
    }
}