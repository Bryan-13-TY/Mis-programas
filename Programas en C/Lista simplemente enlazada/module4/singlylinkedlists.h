#ifndef SINGLYLINKEDLISTS_H
#define SINGLYLINKEDLISTS_H

typedef struct List List;

List *list_create(void);
int obtain_count(List *list);
void insert_end(List *list, int num);
void insert_begin(List *list, int num);
void insert_in_position(List *list, int num, int pos);
void change_value(List *list, int num, int pos);
void search_for_value(List *list, int num);
void search_for_position(List *list, int pos);
void free_list(List *list);
void destroy_list(List *list);
void show_list(List *list);


//void init_list(List *list);
//int obtener_count(List *list);
//void insertar_final(List *list, int num);
//void insertar_inicio(List *list, int num);
//void insertar_posicion(List *list, int num, int pos);
//void sumar_lista(List *list);
//void cambiar_num(List *list, int num, int pos);
//void buscar_num(List* list, int num);
//void consultar_num(List *list, int pos);
//void liberar_num(List *list, int pos);
//void liberar_lista(List *list);
//void mostrar_lista(List *list);

#endif