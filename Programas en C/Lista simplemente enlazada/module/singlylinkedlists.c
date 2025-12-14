#include "singlylinkedlists.h"

#include <stdio.h>
#include <stdlib.h>

static node *head = NULL;
static node *tail = NULL;

/**
 * @brief Crea una lista simplemente enlazada.
 * 
 * Esta función crea el primer número de la lista.
 * 
 * @param num Número inicial de la lista.
 * @param count Puntero al contador de los números en la lista.
 */
static void crear_lista(int num, int *count) {
    head = malloc(sizeof(node)); // nodo inicial de la lista

    if (head == NULL) { // error al crear el nodo
        printf("\n>> ERROR: Error al crear la lista enlazada");
        return;
    }

    head -> num = num;
    head -> sgt = NULL;
    tail = head;

    (*count)++;
}

/**
 * @brief Inserta un número al final de la lista.
 * 
 * Esta función inserta un número al final de la lista, actualizando los enlaces correspondientes.
 * Si la lista esta vacía, se llama a la función CrearLista().
 * 
 * @param num Número a insertar al final de la lista.
 * @param count Puntero al contador de los números en la lista.
 */
void insertar_final(int num, int *count) {
    if (head == NULL) { // lista vacía
        crear_lista(num, count);
        return;
    }

    node *new = malloc(sizeof(node)); // número a insertar

    if (new == NULL) { // error al crear el nodo
        printf("\n>> ERROR: Error al insertar el numero");
        return;
    }

    new -> num = num;
    new -> sgt = NULL;
    tail -> sgt = new;
    tail = new;

    (*count)++;

    printf("\n>> El numero se inserto correctamente");
}

/**
 * @brief Inserta un número al inicio de la lista.
 * 
 * Esta función inserta un número al incio de la lista, actualizando los enlaces correspondientes.
 * Si la lista esta vacía, se llama a la función CrearLista().
 * 
 * @param num Número a insertar al inicio de la lista.
 * @param count Puntero al contador de los números en la lista.
 */
void insertar_inicio(int num, int *count) {
    if (head == NULL) { // lista vacía
        crear_lista(num, count);
        return;
    }

    node *new = malloc(sizeof(node)); // número a insertar

    if (new == NULL) { // error al crear el nodo
        printf("\n>> ERROR: Error al insertar el numero");
        return;
    }

    new -> num = num;
    new -> sgt = head;
    head = new;

    (*count)++;

    printf("\n>> El numero se inserto correctamente");
}

/**
 * @brief Valida la posición en la que se quiere insertar el número.
 * 
 * @param pos Posición en la que se inserta el número.
 * @param count Puntero al contador de los números en la lista.
 */
static bool validar_posicion(int pos, int *count) {
    if (pos > (*count) + 1) {
        printf("\n>> ERROR: No se puede agregar un numero en la posicion %d, ya que no existe la posicion %d", pos, pos - 1);
        return false;
    }
    else if (pos < 1) {
        printf("\n>> ERROR: La posicion %d no es valida", pos);
        return false;
    }

    return true;
}

/**
 * @brief Inserta un número en cualquier posición válida.
 * 
 * Esta función inserta un número en cualquier posición válida de la lista.
 * Si la posición corresponde a la inicial se llama a la función insertar_inicio(),
 * mientras que si corresponde a la final se llama a la función insertar_final().
 * 
 * @param num Número a insertar en una posición de la lista.
 * @param pos Posición en la que se inserta el número.
 * @param count Puntero al contador de los números en la lista.
 */
void insertar_posicion(int num, int pos, int *count) {
    if (!validar_posicion(pos, count)) { // posición no valida
        return;
    }

    if (pos == 1) { // insertar al inicio
        insertar_inicio(num, count);
        return;
    }

    if (pos == *count + 1) { // insertar al final
        insertar_final(num, count);
        return;
    }

    node *new = malloc(sizeof(node)); // número a insertar
    node *before = head; // posición entes de la indicada

    if (new == NULL) {
        printf("\n>> ERROR: Error al insertar el numero");
        return;
    }

    new -> num = num;

    for (int i = 2; i < pos; i++) { // mover *befere a su posición
        before = before -> sgt;
    }

    new -> sgt = before -> sgt;
    before -> sgt = new;

    (*count)++;

    printf("\n>> El numero se inserto correctamente en la posición %d", pos);
}

/**
 * @brief Verifica si la lista esta vacía o no.
 */
static bool vacio() {
    if (head != NULL) {
        return false;
    }

    return true;
}

/**
 * @brief Reemplaza un número de la lista por otro.
 * 
 * Esta función reemplaza cualquier número de la lista en una posición válida de esta. 
 * 
 * @param num Nuevo número en la posición.
 * @param pos Posición en la que se inserta el nuevo número.
 * @param count Puntero al contador de los números en la lista.
 */
void cambiar_num(int num, int pos, int *count) {
    if (vacio()) { // lista vacía
        printf("\n>> ERROR: La lista esta vacia");
        return;
    }

    if (pos > *count || pos < 1) { // posición no válida
        return;
    }

    node *move = head;

    for (int i = 0; i < pos - 1; i++) { // mover *move a su posición
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
void buscar_num(int num) {
    if (vacio()) { // lista vacía
        printf("\n>> ERROR: La lista esta vacia");
        return;
    }

    node *move = head;
    int pos = 0; 
    bool found = false;

    while (move != NULL) { // mover *move a la posición
        if (move -> num == num) { // se encuentra
            found = true;
            printf("\n>> El numero %d se encuentra en la posicion %d de la lista", num, pos + 1);
        }

        move = move -> sgt;
        pos++;
    }

    if (!found) {
        printf("\n>> El numero %d no se encuentra en la lista", num);
    }
}

/**
 * @brief Muestra el número en una posición de la lista.
 * 
 * Esta función recorre la lista hasta la posición indicada y muestra el número alojado en dicha posición.
 * 
 * @param pos Posición del número a consultar.
 * @param count Puntero al contador de los números en la lista.
 */
void consultar_num(int pos, int *count) {
    if (vacio()) {
        printf("\n>> ERROR: La lista esta vacia");
        return;
    }

    if (pos > *count || pos < 1) { // posición no válida
        return;
    }

    node *move = head;

    for (int i = 0; i < pos - 1; i++) { // mover *move a la posición
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
 * @param count Puntero al contador de los números en la lista.
 */
void liberar_num(int pos, int *count) {
    if (vacio()) {
        printf("\n>> ERROR: La lista esta vacia");
        return;
    }
    
    node *move = head;
    node *after = NULL; // apuntador al número anterior al que queremos eliminar
    node *before = NULL; // apuntador al número a eliminar
    node *delete = NULL; // Apuntador al número siguiente al que queremos eliminar

    if (head -> sgt == NULL) { // un elemento en la lista
        free(head);
        head = NULL;
        tail = NULL;

        (*count) = 0;

        printf("\n>> El numero en la posicion %d se elimino correctamente", pos);
        return;
    }

    if (pos == *count) { // último de la lista
        for (int i = 2; i < pos; i++) { // mober *move a la posición
            move = move -> sgt;
        }

        after = move -> sgt; // apuntamos al último
        free(after); // liberamos al último
        tail = move; // actualizamos tail_slist
        tail -> sgt = NULL; // apuntamos a NULL

        (*count)--;

        printf("\n>> El numero en la posicion %d se elimino correctamente", pos);
        return;
    }

    if (pos == 1) { // primero de la lista
        delete = head;
        head = head -> sgt;
        free(delete); // liberamos al número

        (*count)--;

        printf("\n>> El numero en la posicion %d se elimino correctamente", pos);
        return;
    }

    if (pos > *count || pos < 1) { // posición no válida
        return;
    }

    // cualquiera entre head_slits y tail_slits de la lista
    for (int i = 2; i < pos; i++) { // mover *move a la posición anterior
        move = move -> sgt;
    }

    before = move; // apuntamos al aterior
    delete = move -> sgt; // apuntamos al número a eliminar
    after = delete -> sgt; // apuntamos al siguiente
    free(delete); // liberamos al número

    before -> sgt = after; // unimos la lista
    (*count)--;

    printf("\n>> El numero en la posicion %d se elimino correctamente", pos);
}

/**
 * @brief Suma los números de la lista.
 */
void sumar_lista() {
    if (vacio()) { // lista vacía
        printf("\n\n>> ERROR: La lista esta vacia");
        return;
    }

    node *move = head;
    int sum = 0;

    while (move != NULL) {
        sum += move -> num;
        move = move -> sgt;
    }

    printf("\n\n>> La suma de los nomeros de la lista es: %d", sum);
}

/**
 * @brief Borrar tada la lista de números.
 * 
 * @param count Puntero al contador de los números en la lista.
 */
void liberar_lista(int *count) {
    if (vacio()) {
        return;
    }

    node *delete = head;
    node *move = NULL;

    while (delete != NULL) {
        move = delete -> sgt; // nodo siguiente
        free(delete); // liberamos nodo actual
        delete = move; // actualizar
    }

    head = NULL;
    tail = NULL;
    *count = 0;

    printf("\n\n>> La lista se ha eliminado correctamente");
}

/**
 * @brief Imprime la lista.
 */
void mostrar_lista() {
    if (vacio()) {
        printf("\n\n>> ERROR: La lista esta vacia");
        return;
    }

    node *show = head;

    printf("\n\nElementos de la lista: ");

    while (show != NULL) {
        printf("%d -> ", show -> num);
        show = show -> sgt;
    }

    printf("NULL");
}