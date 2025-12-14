#ifndef SINGLYLINKEDLISTS_H
#define SINGLYLINKEDLISTS_H

#include <stdio.h>
#include <stdlib.h>

typedef struct node {
    int num;
    struct node *sgt;
} node;

typedef struct {
    node *head;
    node *tail;
    int count;
} list;

void init_list(list *list);
int obtener_count(list *list);
void insertar_final(list *list, int num);
void insertar_inicio(list *list, int num);
void insertar_posicion(list *list, int num, int pos);
void sumar_lista(list *list);
void cambiar_num(list *list, int num, int pos);
void buscar_num(list* list, int num);
void consultar_num(list *list, int pos);
void liberar_num(list *list, int pos);
void liberar_lista(list *list);
void mostrar_lista(list *list);

#endif