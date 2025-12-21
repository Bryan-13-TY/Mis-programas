#include <stdio.h>
#include <stdlib.h>
#include "singly_lists.h"

int main(int argc, char const *argv[]) {
    int count = 0, pos = 0, sum = 0;
    size_t mem;
    SList *list = slist_create();
    ListStatus st;

    st = slist_insert_end(list, 0); if (st == LIST_OK) printf("\n>> Numero insertado correctamente");
    st = slist_insert_end(list, 10); if (st == LIST_OK) printf("\n>> Numero insertado correctamente");
    st = slist_insert_end(list, 9); if (st == LIST_OK) printf("\n>> Numero insertado correctamente");
    st = slist_insert_end(list, 11); if (st == LIST_OK) printf("\n>> Numero insertado correctamente");
    st = slist_insert_end(list, 20); if (st == LIST_OK) printf("\n>> Numero insertado correctamente");
    //st = insert_end(list, 99); if (st == LIST_OK) printf("\n>> Numero insertado correctamente");
    //st = obtain_count(list, &count); if (st == LIST_OK) printf("\n%d elementos en la lista", count); 
    //show_list(list);
    //st = insert_begin(list, -1); if (st == LIST_OK) printf("\n>> Numero insertado correctamente");
    //st = insert_begin(list, -2); if (st == LIST_OK) printf("\n>> Numero insertado correctamente");
    //show_list(list);
    //st = insert_in_position(list, 100, 9); if (st == LIST_ERR_OUT_OF_RANGE) printf("\n>> Posicion fuera de rango"); 


    slist_show(list);
    st = slist_free_in_position(list, 3);
    if (st == LIST_OK) printf("\n>> Numero eliminado correctamemte");
    if (st == LIST_ERR_OUT_OF_RANGE) printf("\nPosicion no valida");

    st = slist_size(list, &count); if (st == LIST_OK) printf("\nElementos: %d", count);

    st = slist_sum(list, &sum); if (LIST_OK == st) printf("\nLa suma es %d", sum);
    slist_show(list);
    st = slist_size_bytes(list, &mem); if (LIST_OK == st) printf("\nMemoria usada: %zu bytes", mem);

    st = slist_clear(list); if (LIST_OK == st) printf("\nLista vaciada correctemente");
    slist_show(list);
    st = slist_size_bytes(list, &mem); if (LIST_OK == st) printf("\nMemoria usada: %zu bytes", mem);
    st = slist_destroy(list); if (st == LIST_OK) printf("\n>> La lista se elimino correctamente");

    return 0;
}