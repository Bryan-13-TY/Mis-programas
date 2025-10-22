/**
 * @file ParentesisBalanceados.c
 * @brief Verifica el balanceo de paréntesis en una cadena.
 * 
 * Este archivo toma una cadena de paréntesis y usando pilas, determina
 * si la cadena esta balanceada o no.
 * 
 * @author García Escamilla Bryan Alexis
 * @date 2025-10-21
 */

#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <stdbool.h>
#include <string.h>

#define VERSION "1.0"

// Estructra para la pila
typedef struct Node_Stack {
    char bracket;
    struct Node_Stack *sgt;
} Node_Stack;

void push(Node_Stack **stack, char p);
void pop(Node_Stack **stack, char *p);
bool evaluarCadena(char string[], Node_Stack *stack);

// Programa principal
int main(int argc, char const *argv[]) {
    Node_Stack *stack = NULL;
    int op;
    char string[100];

    do  {
        system("cls");
        printf("/*---------------------------------------------.");
        printf("\n| PROGRAMA QUE EVALUA UNA CADENA DE PARENTESIS |");
        printf("\n`---------------------------------------------*/");
        printf("\n\n>> Elija una de las opciones");
        printf("\n\n1.- Evaluar una cadena");
        printf("\n2.- Salir del programa");
        printf("\n\nOpcion: ");
        scanf("%d", &op);

        switch (op) {
            case 1:
                printf("\n__EVALUAR CADENA DE PARENTESIS__");
                
                int c;
                while ((c = getchar()) != '\n' && c != EOF); // Limpia el buffer
            
                printf("\n\nEscribe la cadena a evaluar: ");
                fgets(string, sizeof(string), stdin);
                string[strcspn(string, "\n")] = '\0';

                if (evaluarCadena(string, stack)) {
                    printf("\n>> La cadena de parentesis %s esta balanceada", string);
                } else {
                    printf("\n>> La cadena de parentesis %s no esta balanceada", string);
                }
                getch();
                break;
            case 2:
                printf("\nGracias por probar el programa, vuelva pronto");
                getch();
                break;
            default:
                printf(">> ERROR: La opcion no es valida");
                getch();
                break;
        }
    } while (op != 2);

    return 0;
}

/**
 * @brief Inserta un elemento en la pila.
 * 
 * @param stack Puntero al puntero del tope de la pila.
 * @param p Paréntesis de apertura a insertar en la pila.
 */
void push(Node_Stack **stack, char p) {
    Node_Stack *new = malloc(sizeof(Node_Stack));
    new -> bracket = p;
    new -> sgt = *stack;
    *stack = new;
}

/**
 * @brief Saca un elemento de la pila.
 * 
 * Esta función saca el último elemento agregado a la pila siguiendo el principio LIFO.
 * 
 * @param stack Puntero al puntero del tope de la pila.
 * @param p Puntero al valor del tope de la pila.
 */
void pop(Node_Stack **stack, char *p) {
    Node_Stack *aux = *stack;
    *p = aux -> bracket;
    *stack = aux -> sgt;
    free(aux);
}

/**
 * @brief Verifica el balanceo de una cadena de paréntesis.
 * 
 * Esta función recorre una cadena de paréntesis, guarda en la pila los paréntesis
 * de apertura y saca el último elemento para verificar la correspondencia con la cadena.
 * 
 * @param string Cadena de paréntesis.
 * @param stack Puntero al tope de la pila.
 * 
 * @return true si la pila esta vacía, false en caso contrario.
 */
bool evaluarCadena(char string[], Node_Stack *stack) {
    char p;

    for (int i = 0; string[i] != '\0'; i++) {
        if (string[i] == '(' || string[i] == '{' || string[i] == '[') {
            push(&stack, string[i]);
        } else if (string[i] == ')' || string[i] == '}' || string[i] == ']') {
            if (stack == NULL) return false; // Si la pila está vacía

            pop(&stack, &p); // Sacamos el último paréntesis abierto

            // Verificamos correspondencia
            if (p == '(' && string[i] != ')' ||
                p == '{' && string[i] != '}' ||
                p == '[' && string[i] != ']') {
                return false; // No hay correspondencia
            }
        }
    }

    return (stack == NULL);
}