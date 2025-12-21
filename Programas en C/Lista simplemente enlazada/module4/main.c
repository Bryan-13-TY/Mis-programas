#include "singlylinkedlists.h"

#include <stdio.h>
#include <stdlib.h>
#include <conio.h>

void continue_program() {
    printf("\n\n==> Enter para continuar...");
    getch();
}

int main(int argc, char const *argv[]) {
    int num, op, pos = 0;
    List *list = list_create();

    do {
        system("cls");
        printf("/*--------------------------------------------------------------------.");
        printf("\n| PROGRAMA QUE CREA UNA LISTA DE NUMEROS (LISTA SIMPLEMENTE ENLAZADA) |");
        printf("\n`--------------------------------------------------------------------*/");
        printf("\n\nNumeros en la lista: %d", obtain_count(list));
        printf("\n\n>> Elija una de las opciones");
        printf("\n\n1.- Crear lista");
        printf("\n2.- Insertar un numero al final de la lista");
        printf("\n3.- Insertar un numero al inicio de la lista");
        printf("\n4.- Insertar un numero en una posicion de la lista");
        printf("\n5.- Cambiar un numero de la lista");
        printf("\n6.- Buscar un numero en la lista (por valor)");
        printf("\n7.- Buscar un numero en la lista (pos posicion)");
        printf("\n8.- Borrar un numero en un posicion de la lista");
        printf("\n9.- Sumar los numeros de la lista");
        printf("\n10.- Vaciar lista");
        printf("\n11.- Destruir la lista");
        printf("\n12.- Mostrar la lista");
        printf("\n13.- Salir del programa");
        printf("\n\nOpcion: ");
        scanf("%d", &op);

        switch (op) {
            case 1:
                printf("\n__CREAR LISTA__");
                list = list_create();
                continue_program();
                break;
            case 2:
                printf("\n__INSERTAR UN NUMERO AL FINAL DE LA LISTA__");
                printf("\n\nEscribe el numero a insertar: ");
                scanf("%d", &num);
                insert_end(list, num);
                continue_program();
                break;
            case 3:
                printf("\n__INSERTAR UN NUMERO AL INICIO DE LA LISTA__");
                printf("\n\nEscribe el numero a insertar: ");
                scanf("%d", &num);
                insert_begin(list, num);
                continue_program();
                break;
            case 4:
                printf("\n__INSERTAR UN NUMERO EN UNA POSICION DE LA LISTA__");
                printf("\n\nEscribe la posicion: ");
                scanf("%d", &pos);
                printf("\nEscribe el numero a insertar: ");
                scanf("%d", &num);
                insert_in_position(list, num, pos);
                continue_program();
                break;
            case 5:
                printf("\n__CAMBIAR UN NUMERO DE LA LISTA__");
                printf("\n\nEscribe la posicion: ");
                scanf("%d", &pos);
                printf("\nEscribe el numero a insertar: ");
                scanf("%d", &num);
                change_value(list, num, pos);
                continue_program();
                break;
            case 6:
                printf("\n__BUSCAR UN NUMERO EN LA LISTA (POR NUMERO)__");
                printf("\n\nEscribe el numero a buscar: ");
                scanf("%d", &num);
                //buscar_num(&lista, num);
                continue_program();
                break;
            case 7:
                printf("\n__BUSCAR UN NUMERO EN LA LISTA (POR POSICION)__");
                printf("\n\nEscribe la posicion a consultar: ");
                scanf("%d", &pos);
                //consultar_num(&lista, pos);
                continue_program();
                break;
            case 8:
                printf("\n__BORRAR UN NUMERO EN UNA POSICION DE LA LISTA__");
                printf("\n\nEscribe la posicion del numero a eliminar: ");
                scanf("%d", &pos);
                //liberar_num(&lista, pos);
                continue_program();
                break;
            case 9:
                printf("\n__SUMAR LOS NUMEROS DE LA LISTA__");
                //sumar_lista(&lista);
                continue_program();
                break;
            case 10:
                printf("\n__VACIAR LISTA__");
                free_list(list);
                continue_program();
                break;
            case 11:
                printf("\n__DESTRUIR LISTA__");
                destroy_list(list);
                list = NULL;
                continue_program();
                break;
            case 12:
                printf("\n__MOSTRAR LA LISTA__");
                show_list(list);
                continue_program();
                break;
            case 13:
                printf("\n>> Gracias por probar el programa, regrese pronto");
                //liberar_lista(&lista);
                break;
            default:
                //printf("\n>> ERROR: La opcion no es valida");
                continue_program();
                break;
        }
    } while (op != 13);

    return 0;
}