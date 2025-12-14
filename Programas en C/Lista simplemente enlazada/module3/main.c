#include "singlylinkedlists.h"

#include <stdio.h>
#include <stdlib.h>
#include <conio.h>

int main(int argc, char const *argv[]) {
    List lista;
    int num, op, pos = 0;

    init_list(&lista);

    do {
        system("cls");
        printf("/*--------------------------------------------------------------------.");
        printf("\n| PROGRAMA QUE CREA UNA LISTA DE NUMEROS (LISTA SIMPLEMENTE ENLAZADA) |");
        printf("\n`--------------------------------------------------------------------*/");
        printf("\n\nNumeros en la lista: %d", obtener_count(&lista));
        printf("\n\n>> Elija una de las opciones");
        printf("\n\n1.- Insertar un numero al final de la lista");
        printf("\n2.- Insertar un numero al inicio de la lista");
        printf("\n3.- Insertar un numero en una posicion de la lista");
        printf("\n4.- Cambiar un numero de la lista");
        printf("\n5.- Buscar un numero en la lista (por valor)");
        printf("\n6.- Buscar un numero en la lista (pos posicion)");
        printf("\n7.- Borrar un numero en un posicion de la lista");
        printf("\n8.- Sumar los numeros de la lista");
        printf("\n9.- Borrar la lista");
        printf("\n10.- Mostrar la lista");
        printf("\n11.- Salir del programa");
        printf("\n\nOpcion: ");
        scanf("%d", &op);

        switch (op) {
            case 1:
                printf("\n__INSERTAR UN NUMERO AL FINAL DE LA LISTA__");
                printf("\n\nEscribe el numero a insertar: ");
                scanf("%d", &num);
                insertar_final(&lista, num);
                getch();
                break;
            case 2:
                printf("\n__INSERTAR UN NUMERO AL INICIO DE LA LISTA__");
                printf("\n\nEscribe el numero a insertar: ");
                scanf("%d", &num);
                insertar_inicio(&lista, num);
                getch();
                break;
            case 3:
                printf("\n__INSERTAR UN NUMERO EN UNA POSICION DE LA LISTA__");
                printf("\n\nEscribe la posicion: ");
                scanf("%d", &pos);
                printf("\nEscribe el numero a insertar: ");
                scanf("%d", &num);
                insertar_posicion(&lista, num, pos);
                getch();
                break;
            case 4:
                printf("\n__CAMBIAR UN NUMERO DE LA LISTA__");
                printf("\n\nEscribe la posicion: ");
                scanf("%d", &pos);
                printf("\nEscribe el numero a insertar: ");
                scanf("%d", &num);
                cambiar_num(&lista, num, pos);
                getch();
                break;
            case 5:
                printf("\n__BUSCAR UN NUMERO EN LA LISTA (POR NUMERO)__");
                printf("\n\nEscribe el numero a buscar: ");
                scanf("%d", &num);
                buscar_num(&lista, num);
                getch();
                break;
            case 6:
                printf("\n__BUSCAR UN NUMERO EN LA LISTA (POR POSICION)__");
                printf("\n\nEscribe la posicion a consultar: ");
                scanf("%d", &pos);
                consultar_num(&lista, pos);
                getch();
                break;
            case 7:
                printf("\n__BORRAR UN NUMERO EN UNA POSICION DE LA LISTA__");
                printf("\n\nEscribe la posicion del numero a eliminar: ");
                scanf("%d", &pos);
                liberar_num(&lista, pos);
                getch();
                break;
            case 8:
                printf("\n__SUMAR LOS NUMEROS DE LA LISTA__");
                sumar_lista(&lista);
                getch();
                break;
            case 9:
                liberar_lista(&lista);
                getch();
                break;
            case 10:
                printf("\n__MOSTRAR LA LISTA__");
                mostrar_lista(&lista);
                getch();
                break;
            case 11:
                printf("\n>> Gracias por probar el programa, regrese pronto");
                liberar_lista(&lista);
                getch();
                break;
            default:
                printf("\n>> ERROR: La opcion no es valida");
                getch();
                break;
        }
    } while (op != 11);

    return 0;
}