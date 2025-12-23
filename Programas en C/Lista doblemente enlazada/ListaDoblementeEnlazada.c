/**
 * @file ListaDoblementeEnlazada.c
 * @brief Crea una lista de números doblemente enlazada, con la que se pueden hacer diferentes operaciones.
 * 
 * Este archivo contiene las funciones necesarias para la creación de una lista doblmente enlazada de números, así
 * como aquellas para insertar un número a la lista, ya sea al inicio, final o en cualquier lugar. También contiene
 * funciones para buscar un número en la lista, ya sea por valor o por posición, funciones para reemplazar un número,
 * para eliminar un número o para eliminar toda la lista. Por último la función para imprimir la lista creada.
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

typedef struct Node {
    int num; // Donde se guarda el valor numérico del nodo
    struct Node *sgt; // Puntero a la estructura siguiente
    struct Node *prev; // Puntero a la estructura previa
} Node;

// Punteros
Node *head = NULL; // Cabeza de la lista
Node *tail = NULL; // Cola de la lista

void CrearLista(int num, int *counter);
void InsertarFinal(int num, int *counter);
void InsertarInicio(int num, int *counter);
void InsertarPosicion(int num, int pos, int *counter);
void SumarLista();
void CambiarNum(int num, int pos);
void BuscarNum(int num);
void ConsultarNum(int pos);
void LiberarNum(int pos, int *counter);
void LiberarLista();
void MostrarLista();

// Programa principal
int main(int argc, char const *argv[]) {
    int num, op, pos = 0, counter = 0;
    
    do {
        system("cls");
        printf("/*-------------------------------------------------------------------.");
        printf("\n| PROGRAMA QUE CREA UNA LISTA DE NUMEROS (LISTA DOBLEMENTE ENLAZADA) |");
        printf("\n`-------------------------------------------------------------------*/");
        printf("\n\nNumeros en la lista: %d", counter);
        printf("\n\n>> Elija una de las opciones");
        printf("\n\n1.- Crear la lista de numeros");
        printf("\n2.- Insertar un numero al final de la lista");
        printf("\n3.- Insertar un numero al inicio de la lista");
        printf("\n4.- Insertar un numero en una posicion de la lista (derecha a izquierda)");
        printf("\n5.- Sumar los numeros de la lista");
        printf("\n6.- Cambiar un numero de la lista");
        printf("\n7.- Buscar un numero en la lista (por numero)");
        printf("\n8.- Buscar un numero en la lista (por posicion)");
        printf("\n9.- Borrar un numero en una posicion de la lista");
        printf("\n10.- Borrar la lista");
        printf("\n11.- Mostrar la lista (ambas direcciones)");
        printf("\n12.- Salir del programa");
        printf("\n\nOpcion: ");
        scanf("%d",&op);

        switch (op) {
            case 1:
                if (head == NULL) {
                    printf("\n__CREAR UNA LISTA DE NUMEROS__");
                    printf("\n\nEscribe el numero inicial de la lista: ");
                    scanf("%d", &num);
                    CrearLista(num, &counter);
                } else {
                    printf("\n>> ERROR: La lista ya ha sido creada");
                }
                getch();
                break;
            case 2:
                printf("\n__INSERTAR UN NUMERO AL FINAL DE LA LISTA__");
                printf("\n\nEscribe el numero a insertar: ");
                scanf("%d", &num);
                InsertarFinal(num, &counter);
                getch();
                break;
            case 3:
                printf("\n__INSERTAR UN NUMERO AL INICIO DE LA LISTA__");
                printf("\n\nEscribe el numero a insertar: ");
                scanf("%d", &num);
                InsertarInicio(num, &counter);
                getch();
                break;
            case 4:
                if (head == NULL) {
                    printf("\n>> ERROR: La lista esta vacia");
                } else {
                    printf("\n__INSERTAR UN NUMERO EN UNA POSICION DE LA LISTA (DERECHA A IZQUIERDA)__");
                    printf("\n\nEscribe la posicion: ");
                    scanf("%d", &pos);

                    if (pos > counter + 1) {
                        printf("\n>> ERROR: No se puede agregar un numero en la posicion %d, ya que no existe la posicion %d", pos, pos - 1);
                    }
                    else if (pos < 1) {
                        printf("\n>> ERROR: La posicion %d no es valida", pos);
                    }
                    else {
                        printf("\nEscribe el numero a insertar: ");
                        scanf("%d", &num);
                        InsertarPosicion(num, pos, &counter);
                    }
                }
                getch();
                break;
            case 5:
                if (head == NULL) {
                    printf("\n>> ERROR: La lista esta vacia");
                } else {
                    printf("\n__SUMAR LOS NUMEROS DE LA LISTA__");
                    SumarLista();
                }
                getch();
                break;
            case 6:
                if (head == NULL) {
                    printf("\n>> ERROR: La lista esta vacia");
                } else {
                    printf("\n__CAMBIAR UN NUMERO DE LA LISTA__");
                    printf("\n\nEscribe la posicion: ");
                    scanf("%d", &pos);

                    if (pos > counter || pos < 1) {
                        printf("\n>> ERROR: La posicion %d no es valida", pos);
                    } else {
                        printf("\nEscribe el numero a insertar: ");
                        scanf("%d", &num);
                        CambiarNum(num, pos);   
                    }
                }
                getch();
                break;
            case 7:
                if (head == NULL) {
                    printf("\n>> ERROR: La lista esta vacia");
                } else {
                    printf("\n__BUSCAR UN NUMERO EN LA LISTA (POR NUMERO)__");
                    printf("\n\nEscribe el numero a buscar: ");
                    scanf("%d", &num);
                    BuscarNum(num);
                }
                getch();
                break;
            case 8:
                if (head == NULL) {
                    printf("\n>> ERROR: La lista esta vacia");
                } else {
                    printf("\n__BUSCAR UN NUMERO EN LA LISTA (POR POSICION)__");
                    printf("\n\nEscribe la posicion a consultar: ");
                    scanf("%d", &pos);

                    if (pos < 1 || pos > counter) {
                        printf("\n>> ERROR: La posicion %d no es valida", pos);
                    } else {
                        ConsultarNum(pos);
                    }
                }
                getch();
                break;
            case 9:
                if (head == NULL) {
                    printf("\n>> ERROR: La lista esta vacia");
                }
                else {
                    printf("\n__BORRAR UN NUMERO EN UNA POSICION DE LA LISTA__");
                    printf("\n\nEscribe la posicion del numero a eliminar: ");
                    scanf("%d", &pos);

                    if (pos < 1 || pos > counter) {
                        printf("\n>> ERROR: La posicion %d no es valida", pos);
                    } else {
                        LiberarNum(pos, &counter);
                    }
                }
                getch();
                break;
            case 10:
                if (head == NULL) {
                    printf("\n>> ERROR: La lista esta vacia");
                } else {
                    printf("\n__BORRAR LA LISTA__");
                    LiberarLista();
                    counter = 0;
                }
                getch();
                break;
            case 11:
                if (head == NULL) {
                    printf("\n>> ERROR: La lista esta vacia");
                } else {
                    printf("\n__MOSTRAR LA LISTA (AMBAS DIRECCIONES)__");
                    MostrarLista();
                }
                getch();
                break;
            case 12:
                printf("\n>> Gracias por probar el programa, regrese pronto");
                getch();
                break;
            default:
                printf("\n>> ERROR: La opcion no es valida");
                getch();
                break;
        }
    } while (op != 12);
    return 0;
}

/**
 * @brief Crea una lista doblemente enlazada.
 * 
 * Esta función crea el primer número de la lista.
 * 
 * @param num Número inicial de la lista.
 * @param counter Puntero al contador de los números en la lista.
 */
void CrearLista(int num, int *counter) {
    head = malloc(sizeof(Node)); // Nodo inicial de la lista

    if (head == NULL) { // Verificar si hubo un error al crear el nodo
        printf("\n>> ERROR: Hubo un error al crear la lista");
        return;
    }

    head -> num = num;
    head -> sgt = NULL;
    head -> prev = NULL;
    tail = head;

    (*counter)++;

    printf("\n>> La lista se creo correctamente");
}

/**
 * @brief Inserta un número al final de la lista.
 * 
 * Esta función inserta un número al final de la lista, actualizando los enlaces correspondientes.
 * Si la lista esta vacía, se llama a la función CrearLista().
 * 
 * @param num Número a insertar al final de la lista.
 * @param counter Puntero al contador de los números en la lista.
 */
void InsertarFinal(int num, int *counter) {
    if (head == NULL) { // Verificar si la lista está vacía
        CrearLista(num, counter);
        return;
    }

    Node *new = malloc(sizeof(Node)); // Nuevo número a insertar

    if (new == NULL) { // Verificar si hubo un error al crear el nodo
        printf("\n>> ERROR: Hubo un error al insertar el numero");
        return;
    }

    new -> num = num;
    new -> sgt = NULL;
    new -> prev = tail;
    tail -> sgt = new;
    tail = new;

    (*counter)++;

    printf("\n>> El numero se inserto correctamente al final de la lista");
}

/**
 * @brief Inserta un número al inicio de la lista.
 * 
 * Esta función inserta un número al incio de la lista, actualizando los enlaces correspondientes.
 * Si la lista esta vacía, se llama a la función CrearLista().
 * 
 * @param num Número a insertar al inicio de la lista.
 * @param counter Puntero al contador de los números en la lista.
 */
void InsertarInicio(int num, int *counter) {
    if (head == NULL) { // Verificar si la lista está vacía
        CrearLista(num, counter);
    }

    Node *new = malloc(sizeof(Node)); // Nuevo número a insertar

    if (new == NULL) { // Verificar si hubo un error al crear el nodo
        printf("\n>> ERROR: Hubo un error al insertar el numero");
        return;
    }

    new -> num = num;
    new -> prev = NULL;
    new -> sgt = head;
    head -> prev = new;
    head = new;

    (*counter)++;

    printf("\n>> El numero se inserto correctamente al inicio de la lista");
}

/**
 * @brief Inserta un número en cualquier posición válida.
 * 
 * Esta función inserta un número en cualquier posición válida de la lista.
 * Si la posición corresponde a la inicial se llama a la función InsertarInicio(),
 * mientras que si corresponde a la final se llama a la función InsertarFinal().
 * 
 * @param num Número a insertar en una posición de la lista.
 * @param pos Posición en la que se inserta el número.
 * @param counter Puntero al contador de los números en la lista.
 */
void InsertarPosicion(int num, int pos, int *counter) {
    if (pos == 1) { // Se inserta al incio de la lista
        InsertarInicio(num, counter);
        (*counter)++;
        return;
    }

    if (pos == *counter + 1) { // Se insertar al final de la lista
        InsertarFinal(num, counter);
        (*counter)++;
        return;
    }

    Node *new = malloc(sizeof(Node)); // Nuevo número a insertar 
    Node *before = head; // El número en la posición antes de la indicada
    Node *after = NULL; // El número en la posición después de la indicada

    if (new == NULL) { // Verificar si hubo un error al crear el nodo
        printf("\n>> ERROR: Hubo un error al insertar el numero");
        return;
    }

    new -> num = num;

    for (int i = 2; i < pos; i++) { // Mover before a la posición antes
        before = before -> sgt;
    }

    // Uniendo los siguientes
    new -> sgt = before -> sgt;
    before -> sgt = new;
    
    // Uniendo los previos
    new -> prev = before;
    after = new -> sgt;
    after -> prev = new;
    
    (*counter)++;

    printf("\n>> El numero se inserto correctamente en la posicion %d de la lista", pos);
}

/**
 * @brief Suma los números de la lista.
 */
void SumarLista() {
    Node *move = head;
    int sum = 0;

    while (move != NULL) {
        sum += move -> num;
        move = move -> sgt;
    }

    printf("\n\n>> La suma de los numeros de la lista es: %d", sum);
}

/**
 * @brief Reemplaza un número de la lista por otro.
 * 
 * Esta función reemplaza cualquier número de la lista en una posición válida de esta. 
 * 
 * @param num Nuevo número en la posición.
 * @param pos Posición en la que se inserta el nuevo número.
 */
void CambiarNum(int num, int pos) {
    Node *move = head;

    for (int i = 0; i < pos - 1; i++) { // Mover move a la posición exacta
        move = move -> sgt;
    }

    move -> num = num;

    printf("\n>> El numero en la posicion %d, ha sido modificado correctamente", pos);
}

/**
 * @brief Busca un número en la lista por valor.
 * 
 * Esta función busca un número por valor en la lista e indica la posición en la que se encuentra.
 * 
 * @param num Número a buscar.
 */
void BuscarNum(int num) {
    Node *move = head;
    int pos = 0, flag = 0;

    while (move != NULL) {
        if (move -> num == num) {
            flag = 1;

            printf("\n>> El numero %d se encuentra en la posicion %d de la lista", num, pos + 1);
        }

        move = move -> sgt;
        pos++;
    }

    if (flag == 0) {
        printf("\n>> El numero %d no se encuentra en la lista", num);
    }
}

/**
 * @brief Muestra el número en una posición de la lista.
 * 
 * Esta función recorre la lista hasta la posición indicada y muestra el número alojado en dicha posición.
 * 
 * @param pos Posición del número a consultar.
 */
void ConsultarNum(int pos) {
    Node *move = head;

    for (int i = 0; i < pos - 1; i++) { // Mover move a la posición exacta
        move = move -> sgt;
    }

    printf("\n>> El numero en la posicion %d es el: %d", pos, move -> num);
}

/**
 * @brief Borra cualquier número de la lista.
 * 
 * Esta función elimina cualquier número de la lista en una posición válida.
 * Se considera el caso cuando solo hay un número en la lista, si el número a eliminar
 * es el primero, el último y en cualquier otra posición.
 * 
 * @param pos Posición del número a eliminar.
 * @param counter Puntero al contador de los números en la lista.
 */
void LiberarNum(int pos, int *counter) {
    Node *move = head;
    Node *after = NULL; // Apuntador al número anterior al que queremos eliminar
    Node *before = NULL; // Apuntador al número a eliminar
    Node *delete = NULL; // Apuntador al número siguiente al que queremos eliminar

    if (head -> sgt == NULL) { // Si solo hay un número en la lista
        free(head);
        head = NULL;
        tail = NULL;

        (*counter) = 0;

        printf("\n>> El numero en la posicion %d se elimino correctamente", pos);
        return;
    }

    if (pos == *counter) { // Último número de la lista
        for (int i = 2; i < pos; i++ ) { // Mover move a la posición antes
            move = move -> sgt;
        }

        after = move -> sgt; // Apuntamos al último número
        free(after); // Liberamos el último número
        tail = move; // Actualizamos tail
        tail -> sgt = NULL; // Apuntamos a NULL

        (*counter)--;

        printf("\n>> El numero en la posicion %d se elimino correctamente", pos);
        return;
    }

    if (pos == 1) { // Primer número de la lista
        delete = head;
        head = head -> sgt;
        free(delete); // Liberamos el primer número
        head -> prev = NULL; // Apuntamos a NULL

        (*counter)--;

        printf("\n>> El numero en la posicion %d se elimino correctamente", pos);
        return;
    }

    // Cualquier número entre head y tail de la lista
    for (int i = 0; i < pos - 1; i++) { // Mover move a la posición exacta
        move = move -> sgt;
    }

    delete = move; // Número que queremos eliminar
    before = delete -> prev; // Apuntamos al número anterior
    after = delete -> sgt; // Apuntamos al número siguiente
    free(delete); // Liberamos el número

    before -> sgt = after; // Unimos el anterior con el siguiente
    after -> prev = before; // Unimos el siguiente con el anterior

    (*counter)--;

    printf("\n>> El numero en la posicion %d se elimino correctamente", pos);
}

/**
 * @brief Borrar toda la lista de números.
 */
void LiberarLista() {
    Node *detele = head;
    Node *move = NULL;

    while (detele != NULL) {
        move = detele -> sgt; // Apuntamos al nodo siguiente
        free(detele); // Liberamos el nodo actual
        detele = move; // Actualizamos
    }

    head = NULL;
    tail = NULL;

    printf("\n\n>> La lista se ha eliminado correctamente");
}

/**
 * @brief Imprime la lista en ambos sentidos.
 */
void MostrarLista() {
    Node *right = head;
    Node *left = tail;

    printf("\n\nElementos de la lista: ");
    printf("\n\nDe izquierda a derecha: ");
    printf("NULL <-> ");

    while (right != NULL) {
        printf("%d <-> ", right -> num);
        right = right -> sgt;
    }

    printf("NULL");
    printf("\n\nDe derecha a izquierda: ");
    printf("NULL <-> ");

    while (left != NULL) {
        printf("%d <-> ", left -> num);
        left = left -> prev;
    }

    printf("NULL");
}