#ifndef SINGLYLINKEDLISTS_H
#define SINGLYLINKEDLISTS_H

#include <stdio.h>
#include <stdlib.h>

typedef struct node {
    int num;
    struct node *sgt;
} node;

void insertar_final(int num, int *count);
void insertar_inicio(int num, int *count);
void insertar_posicion(int num, int pos, int *count);
void sumar_lista();
void cambiar_num(int num, int pos, int *count);
void buscar_num(int num);
void consultar_num(int pos, int *count);
void liberar_num(int pos, int *count);
void liberar_lista(int *count);
void mostrar_lista();

#endif