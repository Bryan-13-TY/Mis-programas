/**
 * @file ExpresionesAritmeticas.c
 * @brief Evalua una expresión aritmética.
 * 
 * Este archivo evalua una expresión aritmética usando los operadores "+", "-", "*" y "/"
 * verificando antes de evaluar que los paréntesis (si los tiene) esten balanceados. Y también
 * se considera la división por cero.
 * 
 * @author García Escamilla Bryan Alexis
 * @date 2025-09-08
 */

#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

#define MAX_TOKENS_LEN 10
#define MAX_TOKENS 50

// Estructura para la pila de operadores
typedef struct operatorsStack {
    char operator;
    struct operatorsStack *sgt;
} operatorsStack;

// Estructura para la cola de salida
typedef struct postfixOutput {
    char tokenOutput[10];
    struct postfixOutput *sgt;
} postfixOutput;

// Estructura para la pila del resultado
typedef struct result {
    float num;
    struct result *sgt;
} result;

// Estructura para la pila del balanceo de paréntesis
typedef struct brackets {
    char bracket;
    struct brackets *sgt;
} brackets;

void evaluarExpresion(char expression[], operatorsStack *stack, postfixOutput *head, postfixOutput *tail, result *stackResult, brackets *stackBrackets);
int separarPorTokens(char expression[], char tokens[][10]);
void push(operatorsStack **stack, char p);
void pop(operatorsStack **stack, char *p);
void enqueue(postfixOutput **head, postfixOutput **tail, char token[]);
void dequeue(postfixOutput **head, postfixOutput **tail, char token[]);
bool colaVacia(postfixOutput *head);
int precedencia(char operator);
void pushResult(result **stack, float n);
void popResult(result **stack, float *n);
float resultado(postfixOutput *head, postfixOutput *tail, result *stack);
bool evaluarParentesis(char expression[], brackets *stack);
void pushBrackets(brackets **stack, char p);
void popBrackets(brackets **stack, char *p);

// Programa principal
int main(int argc, char const *argv[]) {
    operatorsStack *stack = NULL;
    postfixOutput *head = NULL;
    postfixOutput *tail = NULL;
    result *stackResult = NULL;
    brackets *stackBrackets = NULL;

    int op;
    char expression[100];

    do {
        system("cls");
        printf("/*--------------------------------------------.");
        printf("\n| PROGRAMA QUE EVALUA EXPRESIONES ARITMETICAS |");
        printf("\n`--------------------------------------------*/");
        printf("\n\n>> Elije una de las opciones");
        printf("\n\n1.- Evaluar una expresion");
        printf("\n2.- Salir del programa");
        printf("\n\nOpcion: ");
        scanf("%d", &op);

        switch (op) {
            case 1:
                printf("\n__EVALUAR UNA EXPRESION ARITMETICA__");

                int c;
                while ((c = getchar()) != '\n' && c != EOF); // Limpia bufer

                printf("\n\nEscribe una expresion: ");
                fgets(expression, sizeof(expression), stdin);
                expression[strcspn(expression, "\n")] = '\0';
                
                evaluarExpresion(expression, stack, head, tail, stackResult, stackBrackets);
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
 * @brief Evalua una expresión aritmética.
 * 
 * Esta función evalua una expresión aritmética, primero verificando si los paréntesis estan balanceados
 * (si los tiene).
 * 
 * @param expression Expresión aritmética a evaluar.
 * @param stack Puntero al tope de la pila de operadores.
 * @param head Puntero a la cabeza de la cola de salida.
 * @param tail Puntero a la cola de la cola de salida.
 * @param stackResult Puntero al tope de la pila del resultado.
 * @param stackBrackets Puntero al tope de la pola de paréntesis.
 */
void evaluarExpresion(char expression[], operatorsStack *stack, postfixOutput *head, postfixOutput *tail, result *stackResult, brackets *stackBrackets) {
    char tokens[MAX_TOKENS][MAX_TOKENS_LEN] = {0};
    char topeValue, token[2] = {0};
    int num_tokens = separarPorTokens(expression ,tokens);

    if (!evaluarParentesis(expression, stackBrackets)) {
        printf("\n>> Syntax error: Los perentesis no estan balanceados");
        return;
    }

    for (int i = 0; i < num_tokens; i++) {
        if (isdigit(tokens[i][0])) { // Si es un número
            enqueue(&head, &tail, tokens[i]);
        } else if (tokens[i][0] == '(') { // Si es un paréntesis de apertura
            push(&stack, tokens[i][0]);
        } else if (tokens[i][0] == ')') { // Si es un peréntesis de cierre
            while (stack != NULL && (stack -> operator) != '(')  {
                pop(&stack, &topeValue);
                token[0] = topeValue; token[1] = '\0';
                enqueue(&head, &tail, token);
            }

            if (stack != NULL && stack -> operator == '(') {
                pop(&stack, &topeValue); // Quitar el '('
            }
        } else if (tokens[i][0] == '+' || tokens[i][0] == '-' ||
            tokens[i][0] == '*' || tokens[i][0] == '/') { // Operador
            while (stack != NULL && stack -> operator != '(' && precedencia(stack -> operator) >= precedencia(tokens[i][0])) {
                pop(&stack, &topeValue);
                token[0] = topeValue; token[1] = '\0';
                enqueue(&head, &tail, token);
            }

            push(&stack, tokens[i][0]);
        }
    }

    while (stack != NULL) { // Se vacía la pila al final
        pop(&stack, &topeValue);
        token[0] = topeValue; token[1] = '\0';
        enqueue(&head, &tail, token);
    }

    float resEv = resultado(head, tail, stackResult);

    if (isnan(resEv)) printf("\n>> Syntax error: Hay una division por cero");
    else printf("\nResultado: %f", resEv);
}

/**
 * @brief Calcula el resultado de la expresión.
 * 
 * Esta funció contiene el procedimiento para calcula el resultado de la expresión.
 * Toma en cuenta la división por cero.
 *  
 * @param head Puntero a la cabeza de la cola de salida.
 * @param tail Puntero a la cola de la cola de salida.
 * @param stack Puntero al tope de la pila de resultado.
 * 
 * @return Resultado de la expresión, de lo contrario NAN.
 */
float resultado (postfixOutput *head, postfixOutput *tail, result *stack) {
    char token[MAX_TOKENS_LEN] = {0};
    float resOp = 0, num = 0, num1 = 0, num2 = 0, resEv = 0;

    while (head != NULL) {
        dequeue(&head, &tail, token);
        
        if (isdigit(token[0])) {
            float x = strtof(token, NULL);
            pushResult(&stack, x);
        } else if (token[0] == '+') {
            popResult(&stack, &num);
            num2 = num;
            popResult(&stack, &num);
            num1 = num; resOp = num1 + num2;
            pushResult(&stack, resOp);
        } else if (token[0] == '-') {
            popResult(&stack, &num);
            num2 = num;
            popResult(&stack, &num);
            num1 = num; resOp = num1 - num2;
            pushResult(&stack, resOp);
        } else if (token[0] == '*') {
            popResult(&stack, &num);
            num2 = num;
            popResult(&stack, &num);
            num1 = num; resOp = num1 * num2;
            pushResult(&stack, resOp);
        } else if (token[0] == '/') {
            popResult(&stack, &num);
            num2 = num; 
            popResult(&stack, &num);
            num1 = num;

            if (num2 == 0) return NAN;
            resOp = num1 / num2;
            pushResult(&stack, resOp);
        }
    }

    resEv = stack -> num;
    return resEv;
}

/**
 * @brief Separa la expresión en tokens.
 * 
 * Esta función recorre y separa la expresión aritmética en tokens para después ser procesada.
 * 
 * @param expression Expresión aritmética a separar.
 * @param tokens Arreglo en donde se guardan los tokens.
 * 
 * @return Cantidad de tokens.
 */
int separarPorTokens(char expression[], char tokens[MAX_TOKENS][MAX_TOKENS_LEN]) {
    int j = 0; // Cantidad de tokens 
    int k = 0; // Tamaño de cada token

    for (int i = 0; expression[i] != '\0'; i++) {
        if (isdigit(expression[i])) { // Si es un dígito
            tokens[j][k++] = expression[i]; // Se acumula un número de más de un dígito
        } else { // Si es un operador o un paréntesis
            if (k > 0) { // Si hay un número en construcción
                tokens[j][k] = '\0'; // Se agrega el carácter nulo al final del número
                j++;
                k = 0;
            }

            if (expression[i] != ' ') {
                // Se guardan los operadores y paréntesis como tokens
                tokens[j][0] = expression[i]; // Se guarda el carácter
                tokens[j][1] = '\0'; // Se agrega el carácter nulo
                j++;
            }
        }
    }

    if (k > 0) { // Si la expresión termina en un número
        tokens[j][k] = '\0';
        j++;
    }

    return j;
}

/**
 * @brief Inserta un operador a la pila de operadores.
 * 
 * @param stack Puntero al puntero al tope de la pila.
 * @param o Operador a insertar en la pila.
 */
void push(operatorsStack **stack, char o) {
    operatorsStack *new = malloc(sizeof(operatorsStack));
    new -> operator = o;
    new -> sgt = *stack;
    *stack = new;
}

/**
 * @brief Saca un operador de la pila de operadores.
 * 
 * @param stack Puntero al puntero al tope de la pila.
 * @param o Puntero al valor del tope de la pila.
 */
void pop(operatorsStack **stack, char *o) {
    operatorsStack *aux = *stack;
    *o = aux -> operator;
    *stack = aux -> sgt;
    free(aux);
}

/**
 * @brief Inserta un número a la pila de resultado.
 * 
 * @param stack Puntero al puntero al tope de la pila.
 * @param n Número a insertar en la pila.
 */
void pushResult(result **stack, float n) {
    result *new = malloc(sizeof(result));
    new -> num = n;
    new -> sgt = *stack;
    *stack = new;
}

/**
 * @brief Saca un número de la pila de operadores.
 * 
 * @param stack Puntero al puntero al tope de la pila.
 * @param n Puntero al valor del tope de la pila.
 */
void popResult(result **stack, float *n) {
    result *aux = *stack;
    *n = aux -> num;
    *stack = aux -> sgt;
    free(aux);
}

/**
 * @brief Verifica si la cola de salida esta vacia.
 * 
 * @param head Puntero a la cabez de la cola de salida.
 * 
 * @return true si esta vacia, false en caso contrario.
 */
bool colaVacia(postfixOutput *head) {
    return (head == NULL)? true : false;
}

/**
 * @brief Inserta un elemento (número u operador) en la cola de salida.
 * 
 * @param head Puntero al puntero a la cabeza de la cola.
 * @param tail Puntero al puntero a la cola de la cola.
 * @param token Número u operad a insertar en la cola.
 */
void enqueue(postfixOutput **head, postfixOutput **tail, char token[]) {
    postfixOutput *new = malloc(sizeof(postfixOutput));
    strcpy(new -> tokenOutput, token);
    new -> sgt = NULL;

    if (colaVacia(*head)) { // Si la cola está vacía
        *head = new;
    } else {
        (*tail) -> sgt = new;
    }

    *tail = new;
}

/**
 * @brief Saca un elemento (número o operador) de la cola de salida.
 * 
 * @param head Puntero al puntero a la cabeza de la cola.
 * @param tail Puntero al puntero a la cola de la cola.
 * @param token Valor de la cola de a cola.
 */
void dequeue(postfixOutput **head, postfixOutput **tail, char token[]) {
    strcpy(token, (*head) -> tokenOutput);
    postfixOutput *aux = *head;

    if (*head == *tail) { // Si hay un solo elemento en la cola
        *head = NULL;
        *tail = NULL;
    } else { // Si hay más de un elemento en la cola
        *head = (*head) -> sgt;
    }

    free(aux);
}

/**
 * @brief Determina la precedencia de los operadores.
 * 
 * @param operator Operador en el tope de la pila de operadores o en el token actual.
 * 
 * @return 2 si el operador tiene más precedencia, 1 en caso contrario.
 */
int precedencia(char operator) {
    if (operator == '+' || operator == '-') {
        return 1;
    } else {
        return 2;
    }
}

/**
 * @brief Determina si los paréntesis (si los tiene) de la expresión están balanceados.
 * 
 * @param expression Expresión aritmética a evaluar.
 * @param stack Puntero al tope de la pila de paréntesis.
 * 
 * @return true si los paréntesis están balanceados, false en caso contrario. 
 */
bool evaluarParentesis(char expression[], brackets *stack) {
    char b;

    for (int i = 0; expression[i] != '\0'; i++) {
        if (expression[i] == '(' || expression[i] == '{' || expression[i] == '[') {
            pushBrackets(&stack, expression[i]);
        } else if (expression[i] == ')' || expression[i] == '}' || expression[i] == ']') {
            if (stack == NULL) return false; // Si la pila está vacía

            popBrackets(&stack, &b); // Sacamos el último paréntesis abierto

            // Verificamos correspondencia
            if (b == '(' && expression[i] != ')' ||
                b == '{' && expression[i] != '}' ||
                b == '[' && expression[i] != ']') {
                return false; // No hay correspondencia
            }
        }
    }

    return (stack == NULL);
}

/**
 * @brief Inserta un paréntesis en la pila de paréntesis.
 * 
 * @param stack Puntero al puntero al tope de la pila.
 * @param b Paréntesis a insertar en la pila.
 */
void pushBrackets(brackets **stack, char b) {
    brackets *new = malloc(sizeof(operatorsStack));
    new -> bracket = b;
    new -> sgt = *stack;
    *stack = new;
}

/**
 * @brief Saca un peréntesis de la piala de paréntesis.
 * 
 * @param stack Puntero al puntero al tope de la pila.
 * @param b Puntero al valor del tope de la pila.
 */
void popBrackets(brackets **stack, char *b) {
    brackets *aux = *stack;
    *b = aux -> bracket;
    *stack = aux -> sgt;
    free(aux);
}