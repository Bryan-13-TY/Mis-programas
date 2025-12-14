#ifndef SINGLYLINKEDLISTS_H
#define SINGLYLINKEDLISTS_H

#include <stdio.h>
#include <stdlib.h>

typedef struct List List;

void init_list(List *list);
int obtener_count(List *list);
void insertar_final(List *list, int num);
void insertar_inicio(List *list, int num);
void insertar_posicion(List *list, int num, int pos);
void sumar_lista(List *list);
void cambiar_num(List *list, int num, int pos);
void buscar_num(List* list, int num);
void consultar_num(List *list, int pos);
void liberar_num(List *list, int pos);
void liberar_lista(List *list);
void mostrar_lista(List *list);

#endif