/**
 * @file Matrices.c
 * @brief Realiza operaciones con dos matrices.
 * 
 * Este archivo contiene las funciones necesarias para hacer sumas, restas
 * multiplicaciones entre dos matrices, para encontrar la matriz transpuesta
 * y la inversa de una matriz.
 * 
 * @note No se ha compilado la última versión de este código. Solo funciona en Windows.
 * 
 * @author García Escamilla Bryan Alexis
 * @date 2025-10-21 
 */

#include <stdio.h>
#include <stdlib.h>
#include <conio.h>

#define VERSION "1.0"
#define SIZE 10 // Tamaño de las matrices

void LeerMatrices(float matrix_1[SIZE][SIZE], float matrix_2[SIZE][SIZE]);
void EscribirMatriz(float matriz[SIZE][SIZE], FILE *output_file);
void ImprimirMatriz(float matrix[SIZE][SIZE]);
void Sumar(float matrix_1[SIZE][SIZE], float matrix_2[SIZE][SIZE]);
void Resta(float matrix_1[SIZE][SIZE], float matrix_2[SIZE][SIZE]);
void Multiplicar(float matrix_1[SIZE][SIZE], float matrix_2[SIZE][SIZE]);
void Transpuesta(float matrix[SIZE][SIZE], char name_file[]);
void Inversa(float matrix[SIZE][SIZE], float matrixi[SIZE][SIZE], char name_file[]);
void Resultados(char name_file[]);

// Programa principal
int main(int argc, char const *argv[]) {
    int op;
    float matrix_1[SIZE][SIZE], matrix_2[SIZE][SIZE], matrix[SIZE][SIZE] = {0};

    do {
        system("cls");
        printf("/*-----------------------------------------------.");
        printf("\n| PROGRAMA QUE HACE OPERACIONES CON DOS MATRICES |");
        printf("\n`-----------------------------------------------*/");
        printf("\n\nLas matrices a operar son:");
        LeerMatrices(matrix_1, matrix_2);
        printf("\n\nMatriz 1:\n\n");
        ImprimirMatriz(matrix_1);
        printf("\nMatriz 2:\n\n");
        ImprimirMatriz(matrix_2);
        printf("\nElija la operacion:");
        printf("\n\n1.- Sumar matrices");
        printf("\n2.- Restar matrices");
        printf("\n3.- Multiplicar matrices");
        printf("\n4.- Transpuesta de matrices");
        printf("\n5.- Inversa de matrices");
        printf("\n6.- Imprimir resuldatos de las operaciones");
        printf("\n7.- Salir del programa");
        printf("\n\nOpcion: ");
        scanf("%d", &op);

        switch (op) {
            case 1:
                printf("\n__SUMA DE MATRICES__");
                printf("\n\nEl resultado de la suma es:\n\n");
                Sumar(matrix_1, matrix_2);
                getch();
                break;
            case 2:
                printf("\n__RESTA DE MATRICES__");
                printf("\n\nEl resultado de la resta es:\n\n");
                Resta(matrix_1, matrix_2);
                getch();
                break;
            case 3:
                printf("\n__MULTIPLICACION DE MATRICES__");
                printf("\n\nEl resultado de la multiplicacion es:\n\n");
                Multiplicar(matrix_1, matrix_2);
                getch();
                break;
            case 4:
                printf("\n__TRANSPUESTA DE LAS MATRICES__");
                printf("\n\nLa transpuesta de la primera matriz es:\n\n");
                Transpuesta(matrix_1, "trans_1.txt");
                printf("\nLa transpuesta de la segunda matriz es:\n\n");
                Transpuesta(matrix_2, "trans_2.txt");
                getch();
                break;
            case 5:
                printf("\n__INVERSA DE LAS MATRICES__");
                printf("\n\nLa inversa de la primera matriz es:\n\n");
                Inversa(matrix_1, matrix,"inv_1.txt");
                printf("\nLa inversa de la segunda matriz es:\n\n");
                Inversa(matrix_2, matrix,"inv_2.txt");
                getch();
                break;
            case 6:
                printf("\n__RESULTADOS__");
                printf("\n\nEl resultado de la suma es:\n\n");
                Resultados("suma.txt");
                printf("\nEl resultado de la resta es:\n\n");
                Resultados("resta.txt");
                printf("\nEl resultado de la multiplicacion es:\n\n");
                Resultados("multi.txt");
                printf("\nLa transpuesta de la primera matriz es:\n\n");
                Resultados("trans_1.txt");
                printf("\nLa transpuesta de la segunda matriz es:\n\n");
                Resultados("trans_2.txt");
                printf("\nLa inversa de la primera matriz es:\n\n");
                Resultados("inv_1.txt");
                printf("\nLa inversa de la segunda matriz es:\n\n");
                Resultados("inv_2.txt");
                getch();
                break;
            case 7:
                printf("\nGracias por probar el programa, vuelva pronto");
                getch();
                break;
            default:
                printf("\nLa opcion no es valida");
                getch();
                break;
        }
    } while(op != 7);

    return 0;
}

/**
 * @brief Lee dos matrices de un archivo.
 * 
 * Esta función lee dos matrices del archivo entrada.txt y las guarda en las matrices correspondientes.
 * 
 * @param matrix_1 Primera matriz leida.
 * @param matrix_2 Segunda matriz leida.
 */
void LeerMatrices(float matrix_1[SIZE][SIZE], float matrix_2[SIZE][SIZE]) {
    FILE *input_file = fopen("entrada.txt", "r");

    if (input_file == NULL) {
        printf("\n\n>> No se puede abrir el archivo que contiene las matrices");
        return;
    }

    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            if (fscanf(input_file, "%f", &matrix_1[i][j]) != 1) {
                printf("\n\n>> Hubo un error al leer la primera matriz");
                fclose(input_file);
                exit(1);
            }
        }
    }

    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            if (fscanf(input_file, "%f", &matrix_2[i][j]) != 1) {
                printf("\n\n>> Hubo un error al leer la segunda matriz");
                fclose(input_file);
                exit(1);
            }
        }
    }

    fclose(input_file);
}

/**
 * @brief Escribe una matriz en un archivo .txt.
 * 
 * @param matrix Matriz a escribir en el archivo.
 * @param output_fila Puntero al archivo.
 */
void EscribirMatriz(float matrix[SIZE][SIZE], FILE *output_file) {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            fprintf(output_file, "[%.0f]", matrix[i][j]);
        }
        fprintf(output_file, "\n");
    }
}

/**
 * @brief Imprime una matriz.
 * 
 * @param matrix Matriz a imprimir.
 */
void ImprimirMatriz(float matrix[SIZE][SIZE]) {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            printf("[%.0f]", matrix[i][j]);
        }
        printf("\n");
    }
}

/**
 * @brief Sumas dos matrices.
 * 
 * Esta función toma dos matrices y las suma, para posteriormente escribir la matriz resultante
 * en el archivo suma.txt con la función EscribirMatriz() y después imprimirla
 * con la función ImprimirMatriz().
 * 
 * @param matrix_1 Primera matriz a sumar.
 * @param matrix_2 Segunda matriz a sumar.
 */
void Sumar(float matrix_1[SIZE][SIZE], float matrix_2[SIZE][SIZE]) {
    float matrix[SIZE][SIZE] = {0};
    FILE *output_file = fopen("suma.txt", "w");

    if (output_file == NULL) {
        printf(">> Hubo un error al abrir el archivo");
        return;
    }

    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            matrix[i][j] = matrix_1[i][j] + matrix_2[i][j];
        }
    }

    EscribirMatriz(matrix, output_file);
    fclose(output_file);
    ImprimirMatriz(matrix);
}

/**
 * @brief Resta dos matrices.
 * 
 * Esta función toma dos matrices y las resta, para posteriormente escribir la matriz resultante
 * en el archivo resta.txt con la función EscribirMatriz() y después imprimirla
 * con la función ImprimirMatriz().
 * 
 * @param matrix_1 Primera matriz a restar.
 * @param matrix_2 Segunda matriz a restar.
 */
void Resta(float matrix_1[SIZE][SIZE], float matrix_2[SIZE][SIZE]) {
    float matrix[SIZE][SIZE] = {0};
    FILE *output_file = fopen("resta.txt", "w");
    
    if (output_file == NULL) {
        printf(">> Hubo un error al abrir el archivo");
        return;   
    }

    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            matrix[i][j] = matrix_1[i][j] - matrix_2[i][j];
        }
    }

    EscribirMatriz(matrix, output_file);
    fclose(output_file);
    ImprimirMatriz(matrix);
}

/**
 * @brief Multiplica dos matrices.
 * 
 * Esta función toma dos matrices y las multiplica, para posteriormente escribir la matriz resultante
 * en el archivo resta.txt con la función EscribirMatriz() y después imprimirla
 * con la función ImprimirMatriz().
 * 
 * @param matrix_1 Primera matriz a multiplicar.
 * @param matrix_2 Segunda matriz a multiplicar.
 */
void Multiplicar(float matrix_1[SIZE][SIZE], float matrix_2[SIZE][SIZE]) {
    float matrix[SIZE][SIZE] = {0};
    FILE *output_file = fopen("multi.txt", "w");

    if (output_file == NULL) {
        printf(">> Hubo un error al abrir el archivo");
        return;   
    }

    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            for (int k = 0; k < SIZE; k++) {
                matrix[i][j] += matrix_1[i][k] * matrix_2[k][j];
            }
        }
    }

    EscribirMatriz(matrix, output_file);
    fclose(output_file);
    ImprimirMatriz(matrix);
}

/**
 * @brief Calcula la transpuesta de una matriz.
 * 
 * Esta función toma una matriz y calcula su transpuesta, para posteriormente escribir la matriz resultante
 * en un archivo .txt con la función EscribirMatriz() y después imprimirla
 * con la función ImprimirMatriz().
 * 
 * @param matrix Matriz a la que se le calcula la transpuesta.
 * @param name_file Nombre del archivo en donde se escribe la transpuesta.
 */
void Transpuesta(float matrix[SIZE][SIZE], char name_file[]) {
    float matrixt[SIZE][SIZE] = {0};
    FILE *output_file = fopen(name_file, "w");
    
    if (output_file == NULL) {
        printf(">> Hubo un error al abrir el archivo");
        return;   
    }

    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            matrixt[i][j] = matrix[i][j];
        }
    }

    EscribirMatriz(matrixt, output_file);
    fclose(output_file);
    ImprimirMatriz(matrixt);
}

/**
 * @brief Calcula la inversa de una matriz.
 * 
 * Esta función toma una matriz y calcula su inversa, para posteriormente escribir la matriz resultante
 * en un archivo .txt con la función EscribirMatriz() y después imprimirla
 * con la función ImprimirMatriz().
 * 
 * Para poderse escribrir la matriz, se verifica que no sea singular de lo contrario
 * esta no tendra inversa.
 * 
 * @param matriz Matriz a la que se le cancula su inversa.
 * @param matrixi Matriz donde se guarda la inversa.
 * @param name_file Nombre del archivo en donde se escribe la inversa.
 */
void Inversa(float matrix[SIZE][SIZE], float matrixi[SIZE][SIZE], char name_file[]) {
    float aux[SIZE][2 * SIZE];
    FILE *output_file = fopen(name_file, "w");

    if (output_file == NULL) {
        printf(">> Hubo un error al abrir el archivo");
        return;   
    }

    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            aux[i][j] = matrix[i][j];
            aux[i][j + SIZE] = (i == j) ? 1 : 0;
        }
    }

    for (int i = 0; i < SIZE; i++) {
        if (aux[i][i] == 0) {
            int exchanged = 0;

            for (int j = i + 1; j < SIZE; j++) {
                if (aux[j][i] != 0) {
                    for (int k = 0; k < 2 * SIZE; k++) {
                        float temp = aux[i][k];
                        aux[i][k] = aux[j][k];
                        aux[j][k] = temp;
                    }

                    exchanged = 1;
                    break;
                }
            }

            if (!exchanged) {
                printf(">> La matriz es singular y no tiene inversa");

                return;
            }
        }

        float pivot = aux[i][i];

        for (int j = 0; j < 2 * SIZE; j++) {
            aux[i][j] /= pivot;
        }

        for (int j = 0; j < SIZE; j++) {
            if (j != i) {
                float factor = aux[j][i];

                for (int k = 0; k < 2 * SIZE; k++) {
                    aux[j][k] -= factor * aux[i][k];
                }
            }
        }
    }

    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            matrixi[i][j] = aux[i][j + SIZE];
        }
    }

    EscribirMatriz(matrixi, output_file);
    fclose(output_file);
    ImprimirMatriz(matrixi);
}

/**
 * @brief Lee y muestra las matrices escritas en los archivos .txt.
 * 
 * @param name_file Nombre del archivo de donde se lee la matriz a mostrar.
 */
void Resultados(char name_file[]) {
    FILE *output_file = fopen(name_file, "r");
    char line[256];

    if (output_file == NULL) {
        printf(">> No se pudo abrir el archivo \n");
        return;
    }

    while (fgets(line, sizeof(line), output_file)) {
        printf("%s", line);
    }

    fclose(output_file);
}