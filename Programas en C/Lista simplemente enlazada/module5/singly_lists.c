#include "singly_lists.h"

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct Node {
    int num;
    struct Node *next;
} Node;

struct SList {
    Node *head;
    Node *tail;
    int count;
};

SList *slist_create(void) {
    SList *list = malloc(sizeof(SList)); // creamos la lista

    if (!list) return NULL;

    list->head = NULL;
    list->tail = NULL;
    list->count = 0;
    return list;
}

ListStatus slist_size(SList *list, int *count) {
    if (!list) return LIST_ERR_NULL;

    *count = list->count;
    return LIST_OK;
}

ListStatus slist_size_bytes(SList *list, size_t *bytes) {
    if (!list) return LIST_ERR_NULL;
    if (!bytes) return LIST_ERR_NULL;

    *bytes = sizeof(SList) + list->count * sizeof(Node);
    return LIST_OK;
}

ListStatus slist_is_empty(SList *list, bool *is_empty) {
    if (!list->head) return LIST_ERR_NULL;

    *is_empty = (list->head == NULL);
    return LIST_OK;
}

ListStatus slist_push_back(SList *list, int num) {
    if (!list) return LIST_ERR_NULL;

    Node *new = malloc(sizeof(Node)); // nuevo nodo
    if (!new) return LIST_ERR_ALLOC;

    new->num = num;
    new->next = NULL;

    if (!list->head) { // lista vacía
        list->head = new;
        list->tail = new;
    } else {
        list->tail->next = new;
        list->tail = new;
    }

    list->count++;
    return LIST_OK;
}

ListStatus slist_push_front(SList *list, int num) {
    if (!list) return LIST_ERR_NULL;

    Node *new = malloc(sizeof(Node)); // nuevo nodo
    if (!new) return LIST_ERR_ALLOC;

    new->num = num;

    if (!list->head) { // lista vacía
        list->head = new;
        list->tail = new;
    } else {
        new->next = list->head;
        list->head = new;
    }

    list->count++;
    return LIST_OK;
}

static ListStatus slist_validate_position(SList *list, int pos, int cond) {
    if (cond == 0) {
        if (pos > list->count + 1 || pos < 1) return LIST_ERR_OUT_OF_RANGE;
    } else {
        if (pos > list->count || pos < 1) return LIST_ERR_OUT_OF_RANGE;
    }

    return LIST_OK;
}

ListStatus slist_insert_in_position(SList *list, int num, int pos) {
    if (!list) return LIST_ERR_NULL;
    if (slist_validate_position(list, pos, 0) != LIST_OK) return LIST_ERR_OUT_OF_RANGE;

    if (pos == 1) { // insertar al inicio
        return slist_insert_begin(list, num);
    }

    if (pos == list->count + 1) { // insertar al final
        return slist_insert_end(list, num);
    }

    // cualquiera entre head y tail

    Node *new = malloc(sizeof(Node)); // número a insertar
    if (!new) return LIST_ERR_ALLOC;

    Node *before_new = list->head; // posición antes de la indicada

    new->num = num;

    for (int i = 2; i < pos; i++) { // mover before_new antes de new
        before_new = before_new->next;
    }

    new->next = before_new->next; // apuntamos al siguiente de new
    before_new->next = new; // apuntamos a new

    list->count++;

    return LIST_OK;
}

ListStatus slist_change_value(SList *list, int num, int pos) {
    if (!list) return LIST_ERR_NULL;
    if (slist_validate_position(list, pos, 1) != LIST_OK) return LIST_ERR_OUT_OF_RANGE;

    Node *actual = list->head;

    for (int i = 0; i < pos - 1; i++) { // mover actua a la posición
        actual = actual->next;
    }

    actual->num = num;
    return LIST_OK;
}

ListStatus slist_search_for_value(SList *list, int num, int *pos) {
    if (!list) return LIST_ERR_NULL;
    if (!list->head) return LIST_ERR_EMPTY;

    Node *actual = list->head;
    int pos_local = 0;
    bool found = false;

    while (actual != NULL) { // mover actual a la posición
        if (actual->num == num) { // se encuentra
            found = true;
            break;
        }

        actual = actual->next;
        pos_local++;
    }

    if (found) {
        *pos = pos_local;
        return LIST_OK;
    }

    return LIST_ERR_NOT_FOUND;
}

ListStatus slist_search_for_position(SList *list, int pos, int *value) {
    if (!list) return LIST_ERR_NULL;
    if (!list->head) return LIST_ERR_EMPTY;
    if (slist_validate_position(list, pos, 1) != LIST_OK) return LIST_ERR_OUT_OF_RANGE;

    Node *actual = list->head;

    for (int i = 0; i < pos - 1; i++) { // mover actual a la posición
        actual = actual->next;
    }

    *value = actual->num;
    return LIST_OK;
}

ListStatus slist_front(SList *list, int *value) {
    if (!list) return LIST_ERR_NULL;
    if (!list->head) return LIST_ERR_NULL;

    *value = list->head->num;
    return LIST_OK;
}
ListStatus slist_back(SList *list, int *value) {
    if (!list) return LIST_ERR_NULL;
    if (!list->tail) return LIST_ERR_NULL;

    *value = list->tail->num;
    return LIST_OK;
}

ListStatus slist_free_in_position(SList *list, int pos) {
    if (!list) return LIST_ERR_NULL;
    if (!list->head) return LIST_ERR_EMPTY;

    Node *actual = list->head;
    Node *after_actual = NULL;
    Node *before_actual = NULL;

    if (pos == list->count) { // último de la lista
        for (int i = 2; i < pos; i++) { // mover actual a la posición anterior
            actual = actual->next;
        }

        after_actual = actual->next; // apuntamos al último
        free(after_actual); // liberamos al último

        list->tail = actual; // actualizamos tail
        list->tail->next = NULL; // apuntamos a NULL
        list->count--;
        return LIST_OK;
    }

    if (pos == 1) { // primero de la lista
        actual = list->head;
        list->head = list->head->next; // actualizamos head
        free(actual); // liberamos al primero
        list->count--;
        return LIST_OK;
    }

    if (slist_validate_position(list, pos, 1) != LIST_OK) return LIST_ERR_OUT_OF_RANGE;

    // cualquiera entre head y tail

    for (int i = 2; i < pos; i++) { // mover acutal a la posición anterior
        actual = actual->next;
    }

    before_actual = actual; // apuntamos al anterior
    after_actual = actual->next->next; // apuntamos al siguiente
    free(actual->next); // liberamos
    before_actual->next = after_actual; // unimos las listas
    list->count--;

    return LIST_OK;
}

ListStatus slist_sum(SList *list, int *sum) {
    if (!list) return LIST_ERR_NULL;
    if (!list->head) return LIST_ERR_EMPTY;

    Node *actual = list -> head;
    int total = 0;

    while (actual != NULL) {
        total += actual->num;
        actual = actual->next;
    }

    *sum = total;
    return LIST_OK;
}

ListStatus slist_clear(SList *list) {
    if (!list) return LIST_ERR_NULL;
    if (!list->head) return LIST_ERR_EMPTY;

    Node *actual = list->head;
    Node *next = NULL;

    while (actual != NULL) {
        next = actual->next; // nodo siguiente
        free(actual); // liberamos nodo actual
        actual = next; // actualizar
    }

    list->head = NULL;
    list->tail = NULL;
    list->count = 0;
    return LIST_OK;
}

ListStatus slist_destroy(SList *list) {
    if (!list) return LIST_ERR_NULL;

    slist_clear(list);
    free(list);
    return LIST_OK;
}

void slist_show(SList *list) {
    Node *actual = list->head;

    printf("\n\nElementos de la lista: ");

    while (actual != NULL) {
        printf("%d -> ", actual->num);
        actual = actual->next;
    }

    printf("NULL");
}