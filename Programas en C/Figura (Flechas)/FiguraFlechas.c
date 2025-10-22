/**
 * @file FiguraFlechas.c
 * @brief Imprime una figura con dos flechas invertidas de diferente tamaño.
 * 
 * Este archivo contiene las funciones necesarias para la impresión de la figura,
 * así como aquellas para calcular valores indispensables para la impresión.
 * 
 * Figura de ejemplo:
 * 
 *     *   *  
 *    ***  *  
 *   *********
 *     *  *** 
 *     *   *  
 * 
 * @note No se ha compilado la última versión de este código. Solo funciona en Windows.
 * 
 * @author García Escamilla Bryan Alexis
 * @date 2025-10-21
 */

#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <string.h>

#define VERSION "1.0"
#define MIN_WIDTH 7
#define MAX_WIDTH 302 // Aumentar de 4 en 4

void CalcularRango(int width, int *height, int *cnst);
void ActualizarAux(int i, int width, int height, int cnst, int *aux, int *aux1, int *aux2, int *aux3);
void CondicionesPrint(int i, int j, int width, int height, int cnst, int aux, int aux1, int aux2, int aux3, FILE *file_figure, int save);
void ImprimirFigura(int width, int height, int cnst, char name_file[], int save);

// Programa principal
int main(int argc, char const *argv[]) {
    int save = 0;
    int width = 0, height = 0, constant = 0, op = 0;
    char name_file[50];
    
    do {
        system("cls");
        printf("/*--------------------------------------------------------------------.");
        printf("\n| PROGRAMA QUE CREA UNA FIGURA DE ACUERDO CON UN NUMERO DE ASTERISCOS |");
        printf("\n`--------------------------------------------------------------------*/");
        printf("\n\nFigura de ejemplo:");
        printf("\n\n   *      *   ");
        printf("\n  ***     *   ");
        printf("\n *****    *   ");
        printf("\n**************");
        printf("\n   *    ***** ");
        printf("\n   *     ***  ");
        printf("\n   *      *   ");
        printf("\n\n1.- Crear la figura");
        printf("\n2.- Salir del programa");
        printf("\n\nOpcion: ");
        scanf("%d", &op);

        switch (op) {
            case 1:
                printf("\n__CREAR FIGURA__");
                printf("\n\nQuiere guardar la figura en un archivo .txt? 1/0: ");
                scanf("%d", &save);

                if (save == 1) {
                    int c;
                    while ((c = getchar()) != '\n' && c != EOF); // Limpia el buffer

                    printf("\nEscribe el nombre del archivo (nombre.txt): ");
                    fgets(name_file, sizeof(name_file), stdin);
                    name_file[strcspn(name_file, "\n")] = '\0';
                }

                printf("\nEscribe el numero de asteriscos de la linea horizontal (%d a %d): ", MIN_WIDTH, MAX_WIDTH);
                scanf("%d", &width);

                if (width >= MIN_WIDTH && width <= MAX_WIDTH) {
                    printf("\nLa figura es la siguiente:\n\n");
                    CalcularRango(width, &height, &constant);
                    ImprimirFigura(width, height, constant, name_file, save);
                } else {
                    printf("\n>> No se permite ese numero de asteriscos");
                }
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
    } while(op != 2);
    
    return 0;
}

/**
 * @brief Calcula la altura de la figura.
 * 
 * Esta función calcula el rango en el que se encuentra el ancho de la figura que ingreso el usuario
 * para calcular la altura de la figura y la constante correspondiente a esa altura.
 * 
 * @param width Ancho de la figura (número de asteriscos de la línea horizontal de la figura).
 * @param height Puntero a la altura que se calcula.
 * @param cnst Puntero a la constante que se calcula.
 */
void CalcularRango(int width, int *height, int *cnst) {
    int total_figures = (MAX_WIDTH - MIN_WIDTH) + 1;
    int min_width = MIN_WIDTH, min = 0, max = 0;
    int total_ranges = total_figures / 4;

    for (int i = 0; i < total_ranges; i++) {
        if (width > min_width - 1 && width < min_width + 4) {
            min = min_width - 1;
            max = min_width + 4;
            *cnst = i + 3; 
        }

        min_width += 4;
    }

    *height = (min / 2) + 2;
}

/**
 * @brief Actualiza las variables auxiliares de impresión.
 * 
 * Esta función actualiza el valor de las variables auxiliares de impresión dependiendo
 * de si la fila (i) actual es mayor o menor a la mitad de la altura de la figura.
 * 
 * @param i Fila actual que se esta imprimiendo (empieza desde cero).
 * @param width Ancho de la figura (número de asteriscos de la línea horizontal de la figura).
 * @param height Altura de la figura.
 * @param cnst Constante correspondiente a la altura.
 * @param aux Puntero a la variable auxiliar de impresión para la parte izquierda de la flecha de arriba de la figura.
 * @param aux1 Puntero a la variable auxliar de impresión para la parte derecha de la flecha de abajo de la figura.
 * @param aux2 Puntero a la variable auxiliar de impresión para la parte izquierda de la flecha de abajo de la figura.
 * @param aux3 Puntero a la variable auxiliar de impresión para la parte derecha de la flecha de arriba de la figura.
 */
void ActualizarAux(int i, int width, int height, int cnst, int *aux, int *aux1, int *aux2, int *aux3) {
    if (i < (height / 2)) {
        (*aux)--;
        (*aux3)++;
    } else {
        *aux = height;
        *aux3 = (height + cnst) + 1;
    }

    if (i > (height / 2)) {
        (*aux1)--;
        (*aux2)++;
    } else {
        *aux1 = width - 1;
        *aux2 = ((width - cnst) - (height - cnst)) + 1;
    }
}

/**
 * @brief Contiene las condiciones de impresión de la figura.
 * 
 * Esta función imprime los asteriscos (*) y los espacios ( ) de acuerda a las condiciones
 * para cada cuadrante de la figura. Se usan las variables auxiliares de impresión para ello, así
 * como el ancho, la altura y su constante correspondiente. 
 * 
 * Se hace lo mismo para un archivo .txt con un nombre personalizado, de acuerdo con el valor de la varable save.
 * 
 * @param i Fila actual que se esta imprimiendo (empieza desde cero).
 * @param j Columna actual que se esta imprimiendo (empieza desde cero).
 * @param width Ancho de la figura (número de asteriscos de la línea horizontal de la figura).
 * @param height Altura de la figura.
 * @param cnst Constante correspondiente a la altura.
 * @param aux Variable auxiliar de impresión para la parte izquierda de la flecha de arriba de la figura.
 * @param aux1 Variable auxliar de impresión para la parte derecha de la flecha de abajo de la figura.
 * @param aux2 Variable auxiliar de impresión para la parte izquierda de la flecha de abajo de la figura.
 * @param aux3 Variable auxiliar de impresión para la parte derecha de la flecha de arriba de la figura.
 * @param file_figure Puntero al archivo donde se imprime la figura.
 * @param save Indica la impresión de la figura en un archivo .txt si esta es 1.
 */
void CondicionesPrint(int i, int j, int width, int height, int cnst, int aux, int aux1, int aux2, int aux3, FILE *file_figure, int save) {
    if (j < (height - cnst) && i < (height / 2)) { // 1er cuadrante de arriba
        // Imprime la parte izquierda de la flecha de arriba
        if (j < (aux - cnst)) {
            printf(" ");
            if (save == 1) fprintf(file_figure, " ");
            return;
        }

        printf("*");
        if (save == 1) fprintf(file_figure, "*");
        return;
    }

    if (j < (height - cnst) && i > (height / 2)) { // 1er cuadrante de abajo
        printf(" ");
        if (save == 1) fprintf(file_figure, " ");
        return;
    }

    if (j > (height - cnst) && j < (width - cnst) && i > (height / 2)) { // 2do cuadrante de abajo
        // Imprime la parte izquierda de la flecha de abajo
        if (j < aux2) {
            printf(" ");
            if (save == 1) fprintf(file_figure, " ");
            return;
        }

        printf("*");
        if (save == 1) fprintf(file_figure, "*");
        return;
    }

    if (j > (height - cnst) && j < (width - cnst) && i < (height / 2)) { // 2do cuadrante de arriba
        // Imprime la parte derecha de la flecha de arriba
        if (j < aux3) {
            printf("*");
            if (save == 1) fprintf(file_figure, "*");
            return;
        }

        printf(" ");
        if (save == 1) fprintf(file_figure, " ");
        return;
    }

    if (j > (width - cnst) && i < (height / 2)) { // 3er cuadrante de arriba
        printf(" ");
        if (save == 1) fprintf(file_figure, " ");
        return;
    }

    if (j > (width - cnst) && i > (height / 2)) { // 3er cuadrante de abajo
        // Imprime la parte derecha de la flecha de abajo
        if (j < aux1) {
            printf("*");
            if (save == 1) fprintf(file_figure, "*");
            return;
        }

        printf(" ");
        if (save == 1) fprintf(file_figure, " ");
        return;
    }

    printf("*");
    if (save == 1) fprintf(file_figure, "*");
}

/**
 * @brief Imprime la figura.
 * 
 * Esta función define los valores iniciales de las variables auxiliares de impresión e imprime la figura.
 * 
 * @param width Ancho de la figura (número de asteriscos de la línea horizontal de la figura).
 * @param height Altura de la figura.
 * @param cnst Constante correspondiente a la altura.
 * @param name_file Nombre del archivo donde se imprime la figura.
 * @param save Indica la impresión de la figura en un archivo .txt si esta es 1.
 */
void ImprimirFigura(int width, int height, int cnst, char name_file[], int save) {
    // Se definen variables auxiliares
    int aux_print = height;
    int aux_print1 = width - 1;
    int aux_print2 = ((width - cnst) - (height - cnst)) + 1;
    int aux_print3 = (height - cnst) + 1;
    FILE *file_figure;
    file_figure = fopen(name_file, "w");
    
    for (int i = 0; i < height; i++) { // Filas
        for (int j = 0; j < width; j++) { // Columnas
            CondicionesPrint(i, j, width, height, cnst, aux_print, aux_print1, aux_print2, aux_print3, file_figure, save);
        }

        printf("\n");
        if (save == 1) fprintf(file_figure, "\n");
        ActualizarAux(i, width, height, cnst, &aux_print, &aux_print1, &aux_print2, &aux_print3);
    }

    fclose(file_figure);
    if (save == 1) printf("\nLa figura se guardo en el archivo %s correctamente", name_file);
}