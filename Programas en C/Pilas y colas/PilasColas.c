/**
 * @file PilasColas.c
 * @brief Crea una pila y una cola simples.
 * 
 * Este archivo contiene un menú que permite elegir trabajar con pilas o colas.
 * También contiene las dos operaciones para pilas (push y pop) y para colas (enqueue y dequeue).
 * 
 * @author García Escamilla Bryan Alexis
 * @date 2025-08-26
 */

#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <stdbool.h>

// Estructura para la pila
typedef struct Node_Stack {
    int num;
    struct Node_Stack *sgt;
} Node_Stack;

// Estructura para la cola
typedef struct Node_Queue  {
    int num;
    struct Node_Queue *sgt;
} Node_Queue;

void Menu_Pila(Node_Stack *stack);
void Menu_Cola(Node_Queue *head, Node_Queue *tail);
void Push(Node_Stack **stack, int num);
void Pop(Node_Stack **stack, int *num);
void Enqueue(Node_Queue **head, Node_Queue **tail, int num);
void Dequeue(Node_Queue **head, Node_Queue **tail, int *num);
bool ColaVacia(Node_Queue *head);

// Programa principal
int main(int argc, char const *argv[]) {
    Node_Stack *stack = NULL;
    Node_Queue *head = NULL;
    Node_Queue *tail = NULL;
    int op;

    do {
        system("cls");
        printf("/*--------------------------------------.");
        printf("\n| PROGRAMA QUE CREA UNA PILA Y UNA COLA |");
        printf("\n`--------------------------------------*/");
        printf("\n\n>> Elija una de las opciones");
        printf("\n\n1.- Pila");
        printf("\n2.- Cola");
        printf("\n3.- Salir del programa");
        printf("\n\nOpcion: ");
        scanf("%d", &op);

        switch (op) {
            case 1:
                Menu_Pila(stack);
                break;
            case 2:
                Menu_Cola(head, tail);
                break;
            case 3:
                printf("\n>> Gracias por probar el programa, regrese pronto");
                getch();
                break;
            default:
                printf("\n>> ERORR: La opción no es valida");
                getch();
                break;
        }
    } while (op != 3);

    return 0;
}

/**
 * @brief Menú para la pila.
 * 
 * Esta función contiene el menú para la pila en donde se elige entre sus dos operaciones.
 * 
 * @param stack Puntero a la pila.
 */
void Menu_Pila(Node_Stack *stack) {
    int op, num = 0;

    do {
        system("cls");
        printf("/*------.");
        printf("\n| PILAS |");
        printf("\n`------*/");
        printf("\n\n>> Elija una de las opciones");
        printf("\n\n1.- Agregar un elemento en la pila");
        printf("\n2.- Mostrar los elementos de la pila");
        printf("\n3.- Regresar");
        printf("\n\nOpcion: ");
        scanf("%d", &op);

        switch (op) {
            case 1:
                printf("\n__AGREGAR UN ELEMENTO A LA PILA__");
                printf("\n\nEscribe el numero a agregar: ");
                scanf("%d", &num);
                Push(&stack, num);
                getch();
                break;
            case 2:
                printf("\n__MOSTRAR LOS ELEMENTOS DE LA PILA__");

                if (stack == NULL) {
                    printf("\n\n>> ERROR: La pila esta vacia");
                } else {
                    printf("\n\nLos elementos de la pila son: ");
                    
                    while (stack != NULL) {
                        Pop(&stack, &num);

                        if (stack != NULL) {
                            printf("%d , ", num);

                        } else {
                            printf("%d.", num);
                        }
                    }
                }
                getch();
                break;
            case 3:
                break;
            default:
                printf("\n>> ERORR: La opción no es valida");
                getch();
                break;
        }
    } while (op != 3);
}

/**
 * @brief Menú para la cola.
 * 
 * Esta función contiene el menú para la cola en donde se elige entre sus dos operaciones.
 * 
 * @param head Puntero a la cabeza de la cola.
 * @param tail Puntero a la cola de la cola.
 */
void Menu_Cola(Node_Queue *head, Node_Queue *tail) {
    int op, num = 0;

    do { 
        system("cls");
        printf("/*------.");
        printf("\n| COLAS |");
        printf("\n`------*/");
        printf("\n\n>> Elija una de las opciones");
        printf("\n\n1.- Agregar un elemento a la cola");
        printf("\n2.- Mostrar los elementos de la cola");
        printf("\n3.- Regresar");
        printf("\n\nOpcion: ");
        scanf("%d", &op);

        switch (op) {
            case 1:
                printf("\n__AGREGAR UN ELEMENTO A LA COLA__");
                printf("\n\nEscribe el numero a agregar: ");
                scanf("%d", &num);
                Enqueue(&head, &tail, num);
                getch();
                break;
            case 2:
                printf("\n__MOSTRAR LOS ELEMENTOS DE LA COLA__");
                
                if (head == NULL) {
                    printf("\n\n>> ERROR: La cola esta vacia");
                } else {
                    printf("\n\nLos elemenetos de la cola son: ");
                    
                    while (head != NULL) {
                        Dequeue(&head, &tail, &num);

                        if (head != NULL) {
                            printf("%d , ", num);
                        } else {
                            printf("%d.", num);
                        }
                    }
                }
                getch();
                break;
            case 3:
                break;
            default:
                printf("\n>> ERORR: La opción no es valida");
                getch();
                break;
        }
    } while (op != 3);
}

/**
 * @brief Inserta un número a la pila.
 * 
 * @param stack Puntero al puntero de la pila.
 * @param num Número a insertar en la pila.
 */
void Push(Node_Stack **stack, int num) {
    Node_Stack *new = malloc(sizeof(Node_Stack));
    new -> num = num;
    new -> sgt = *stack;
    *stack = new;

    printf("\n>> El numero %d ha sido agregado a la pila correctamente", num);
}

/**
 * @brief Saca un número de la pila,
 * 
 * Esta función saca un número de la pila siguiendo el principio LIFO.
 * 
 * @param stack Puntero al puntero de la pila.
 * @param num Puntero al valor de un elemento de la pila.
 */
void Pop(Node_Stack **stack, int *num) {
    Node_Stack *aux = *stack;
    *num = aux -> num;
    *stack = aux -> sgt;
    free(aux); 
}

/**
 * @brief Verifica si la cola esta vacía.
 * 
 * @param head Puntero a la cabeza de la cola.
 * 
 * @return True si la cola esta vacía, False en caso contrario.
 */
bool ColaVacia(Node_Queue *head) {
    return (head == NULL)? true : false;
}

/**
 * @brief Inserta un número en la cola.
 * 
 * @param head Puntero al puntero de la cabeza de la cola.
 * @param tail Puntero al puntero de la cola de la cola.
 * @param num Número a insertar en la cola.
 */
void Enqueue(Node_Queue **head, Node_Queue **tail, int num) {
    Node_Queue *new = malloc(sizeof(Node_Queue));
    new -> num = num;
    new -> sgt = NULL;

    if (ColaVacia(*head)) { // Si la cola esta vacía.
        *head = new;
    } else {
        (*tail) -> sgt = new;
    }

    *tail = new;

    printf("\n>> El numero %d ha sido agregado a la cola correctamente", num);
}

/**
 * @brief Saca un número de la cola.
 * 
 * Esta función saca un número de la cola siguiendo el principio FIFO.
 * 
 * @param head Puntero al puntero de la cabeza de la cola.
 * @param tail Puntero al puntero de la cola de la cola.
 * @param num Puntero al valor de un elemento de la cola.
 */
void Dequeue(Node_Queue **head, Node_Queue **tail, int *num) {
    *num = (*head) -> num;
    Node_Queue *aux = *head;

    if (*head == *tail) { // Si hay un solo elemento en la cola
        *head = NULL;
        *tail = NULL;
    } else { // Si hay más de un elemento en la cola.
        *head = (*head) -> sgt;
    }

    free(aux);
}