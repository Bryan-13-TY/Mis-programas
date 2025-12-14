#include "singlylinkedlists.h"

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

void init_list(list *list) {
    list -> head = NULL;
    list -> tail = NULL;
    list -> count = 0;
}

int obtener_count(list *list) {
    return list -> count;
}

/**
 * @brief Crea una lista simplemente enlazada.
 * 
 * Esta función crea el primer número de la lista.
 * 
 * @param num Número inicial de la lista.
 * @param count Puntero al contador de los números en la lista.
 */
static void crear_lista(list *list, int num) {
    list -> head = malloc(sizeof(node)); // nodo inicial de la lista

    if (list -> head == NULL) { // error al crear el nodo
        printf("\n>> ERROR: Error al crear la lista enlazada");
        return;
    }

    list -> head -> num = num;
    list -> head -> sgt = NULL;
    list -> tail = list -> head;

    list -> count++;

    printf("\n>> El numero %d se inserto correctamente", num);
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
void insertar_final(list *list, int num) {
    if (list -> head == NULL) { // lista vacía
        crear_lista(list, num);
        return;
    }

    node *new = malloc(sizeof(node)); // número a insertar

    if (new == NULL) { // error al crear el nodo
        printf("\n>> ERROR: Error al insertar el numero");
        return;
    }

    new -> num = num;
    new -> sgt = NULL;
    list -> tail -> sgt = new;
    list -> tail = new;

    list -> count++;

    printf("\n>> El numero %d se inserto correctamente", num);
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
void insertar_inicio(list *list, int num) {
    if (list -> head == NULL) { // lista vacía
        crear_lista(list, num);
        return;
    }

    node *new = malloc(sizeof(node)); // número a insertar

    if (new == NULL) { // error al crear el nodo
        printf("\n>> ERROR: Error al insertar el numero");
        return;
    }

    new -> num = num;
    new -> sgt = list -> head;
    list -> head = new;

    list -> count++;

    printf("\n>> El numero %d se inserto correctamente", num);
}

/**
 * @brief Valida la posición en la que se quiere insertar el número.
 * 
 * @param pos Posición en la que se inserta el número.
 * @param count Puntero al contador de los números en la lista.
 */
static bool validar_posicion(list *list, int pos) {
    if (pos > list -> count + 1) {
        printf("\n>> ERROR: La posicion %d no es valida", pos);
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
void insertar_posicion(list *list, int num, int pos) {
    if (!validar_posicion(list, pos)) { // posición no valida
        return;
    }

    if (pos == 1) { // insertar al inicio
        insertar_inicio(list, num);
        return;
    }

    if (pos == list -> count + 1) { // insertar al final
        insertar_final(list, num);
        return;
    }

    node *new = malloc(sizeof(node)); // número a insertar
    node *before = list -> head; // posición entes de la indicada

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

    list -> count++;

    printf("\n>> El numero %d se inserto correctamente", num);
}

/**
 * @brief Verifica si la lista esta vacía o no.
 */
static bool vacio(list *list) {
    if (list -> head != NULL) {
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
void cambiar_num(list *list, int num, int pos) {
    if (vacio(list)) { // lista vacía
        printf("\n>> ERROR: La lista esta vacia");
        return;
    }

    if (pos > list -> count || pos < 1) { // posición no válida
        printf("\n>> ERROR: Posicion no valida");
        return;
    }

    node *actual = list -> head;

    for (int i = 0; i < pos - 1; i++) { // mover *move a su posición
        actual = actual -> sgt;
    }

    actual -> num = num;

    printf("\n>> El numero en la posicion %d, ha sido modificado correctamente", pos);
}

/**
 * @brief Busca un número en la lista por valor.
 * 
 * Esta función busca un número por valor en la lista e indica la posición en la que se encuentra.
 * 
 * @param num Número a buscar.
 */
void buscar_num(list *list, int num) {
    if (vacio(list)) { // lista vacía
        printf("\n>> ERROR: La lista esta vacia");
        return;
    }

    node *actual = list -> head;
    int pos = 0; 
    bool found = false;

    while (actual != NULL) { // mover *move a la posición
        if (actual -> num == num) { // se encuentra
            found = true;
            printf("\n>> El numero %d se encuentra en la posicion %d de la lista", num, pos + 1);
        }

        actual = actual -> sgt;
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
void consultar_num(list *list, int pos) {
    if (vacio(list)) {
        printf("\n>> ERROR: La lista esta vacia");
        return;
    }

    if (pos > list -> count || pos < 1) { // posición no válida
        printf("\n>> ERROR: Posicion no valida");
        return;
    }

    node *actual = list -> head;

    for (int i = 0; i < pos - 1; i++) { // mover *move a la posición
        actual = actual -> sgt;
    }

    printf("\n>> El numero en la posicion %d es el %d", pos, actual -> num);
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
void liberar_num(list *list, int pos) {
    if (vacio(list)) {
        printf("\n>> ERROR: La lista esta vacia");
        return;
    }
    
    node *actual = list -> head;
    node *after = NULL; // apuntador al número anterior al que queremos eliminar
    node *before = NULL; // apuntador al número a eliminar
    node *delete = NULL; // Apuntador al número siguiente al que queremos eliminar

    if (list -> head -> sgt == NULL) { // un elemento en la lista
        free(list -> head);
        list -> head = NULL;
        list -> tail = NULL;

        list -> count = 0;

        printf("\n>> El numero se elimino correctamente");
        return;
    }

    if (pos == list -> count) { // último de la lista
        for (int i = 2; i < pos; i++) { // mober *move a la posición
            actual = actual -> sgt;
        }

        after = actual -> sgt; // apuntamos al último
        free(after); // liberamos al último
        list -> tail = actual; // actualizamos tail_slist
        list -> tail -> sgt = NULL; // apuntamos a NULL

        list -> count--;

        printf("\n>> El numero se elimino correctamente");
        return;
    }

    if (pos == 1) { // primero de la lista
        delete = list -> head;
        list -> head = list -> head -> sgt;
        free(delete); // liberamos al número

        list -> count--;

        printf("\n>> El numero se elimino correctamente");
        return;
    }

    if (pos > list -> count || pos < 1) { // posición no válida
        printf("\n>> ERROR: Posicion no valida");
        return;
    }

    // cualquiera entre head y tail de la lista
    for (int i = 2; i < pos; i++) { // mover *move a la posición anterior
        actual = actual -> sgt;
    }

    before = actual; // apuntamos al aterior
    delete = actual -> sgt; // apuntamos al número a eliminar
    after = delete -> sgt; // apuntamos al siguiente
    free(delete); // liberamos al número

    before -> sgt = after; // unimos la lista
    list -> count--;

    printf("\n>> El numero se elimino correctamente");
}

/**
 * @brief Suma los números de la lista.
 */
void sumar_lista(list *list) {
    if (vacio(list)) { // lista vacía
        printf("\n\n>> ERROR: La lista esta vacia");
        return;
    }

    node *actual = list -> head;
    int sum = 0;

    while (actual != NULL) {
        sum += actual -> num;
        actual = actual -> sgt;
    }

    printf("\n\n>> La suma de los numeros de la lista es %d", sum);
}

/**
 * @brief Borrar tada la lista de números.
 * 
 * @param count Puntero al contador de los números en la lista.
 */
void liberar_lista(list *list) {
    if (vacio(list)) {
        return;
    }

    node *delete = list -> head;
    node *actual = NULL;

    while (delete != NULL) {
        actual = delete -> sgt; // nodo siguiente
        free(delete); // liberamos nodo actual
        delete = actual; // actualizar
    }

    list -> head = NULL;
    list -> tail = NULL;
    list -> count = 0;

    printf("\n>> La lista se ha eliminado correctamente");
}

/**
 * @brief Imprime la lista.
 */
void mostrar_lista(list *list) {
    if (vacio(list)) {
        printf("\n\n>> ERROR: La lista esta vacia");
        return;
    }

    node *actual = list -> head;

    printf("\n\nElementos de la lista: ");

    while (actual != NULL) {
        printf("%d -> ", actual -> num);
        actual = actual -> sgt;
    }

    printf("NULL");
}