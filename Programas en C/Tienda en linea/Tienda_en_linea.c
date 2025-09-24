#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <string.h>

// Estructura para la tienda en línea
typedef struct onlineStore {
    char nameArticle[100]; // Nombre del artículo
    char category[30]; // Tipo/categoría del artículo
    char brand[20]; // Marca del artículo
    float price; // Precio del artículo
    char currency[20]; // Tipo de moneda del artículo
    int availableItems; // Cantidad de artículos disponibles
    struct onlineStore *sgt;
} onlineStore; 

// Estructura para el carrito de compra
typedef struct cart {
    char nameProduct[100]; // Nombre del artículo
    char category[30]; // Tipo/categoría del artículo
    float price; // Precio del artículo
    int orderedItems; // Cantidad de artículos pedidos
    struct cart *sgt;
} cart;

// Punteros
onlineStore *sHead = NULL;
onlineStore *sTail = NULL;
cart *cHead = NULL;
cart *cTail = NULL;

// Prototipos de funciones
void readString(int size, char string[size]);
void cleanBuffer();
void storeMenu();
void customerMenu();

// Programa principal
int main(int argc, char const *argv[]) {
    int op = 0;

    do {
        system("cls");
        printf("/*----------------.");
        printf("\n| TIENDA EN LINEA |");
        printf("\n`----------------*/");
        printf("\n\n>> Elija una de las opciones");
        printf("\n\n1.- Tienda");
        printf("\n2.- Cliente");
        printf("\n3.- Salir del programa");
        printf("\n\nOpcion: ");
        scanf("%d", &op);
        cleanBuffer();

        switch (op) {
            case 1:
                storeMenu();
                break;
            case 2:
                customerMenu();
                break;
            case 3:
                printf("\n>> Gracias por probar el programa, regrese pronto");
                getch();
                break;
            default:
                printf("\n>> ERROR: La opcion no es valida");
                getch();
                break;
        }
    } while (op != 3);

    return 0;
}

void readString(int size, char string[size]) {
    fgets(string, size, stdin);
    string[strcspn(string, "\n")] = '\0';
}

void cleanBuffer() {
    int c;

    while ((c = getchar()) != '\n' && c != EOF);
}

void storeMenu() {
    int op = 0, availableItems = 0;
    char nameArticle[100], category[30], brand[20], currency[20];
    float price = 0;

    do {
        system("cls");
        printf("/*------------------.");
        printf("\n| MENU DE LA TIENDA |");
        printf("\n`------------------*/");
        printf("\n\n>> Elija una de las opciones");
        printf("\n\n1.- Agregar un articulo a la tienda");
        printf("\n2.- Modificar un articulo de la tienda");
        printf("\n3.- Mostrar articulos de la tienda");
        printf("\n4.- Volver");
        printf("\n\nOpcion: ");
        scanf("%d", &op);
        cleanBuffer();

        switch (op) {
            case 1:
                printf("\n__AGREGAR UN ARTICULO A LA TIENDA__");
                printf("\n\nEscribe el nombre del articulo: ");
                readString(sizeof(nameArticle), nameArticle);
                printf("\nEscribe la categoria del articulo: ");
                readString(sizeof(category), category);
                printf("\nEscribe la marca del articulo: ");
                readString(sizeof(brand), brand);
                printf("\nEscribe el precio del articulo: ");
                scanf("%f", &price);
                cleanBuffer();
                printf("\nEscribe el tipo de moneda: ");
                readString(sizeof(currency), currency);
                printf("\nEscribe el numero de articulos: ");
                scanf("%d", &availableItems);
                cleanBuffer(); 

                printf("\nNombre del articulo: %s", nameArticle);
                printf("\nCategoria: %s", category);
                printf("\nMarca: %s", brand);
                printf("\nPrecio: %f", price);
                printf("\nMoneda: %s", currency);
                printf("\nCamtidad: %d", availableItems);
                getch();
                break;
            case 2:
                break;
            case 3:
                break;
            case 4:
                break;
            default:
                break;
        }
    } while (op != 4);
}

void customerMenu() {
    int op = 0;

    do {
        system("cls");
        printf("/*-----------------.");
        printf("\n| MENU DEL CLIENTE |");
        printf("\n`-----------------*/");
    } while (op != 4);
}