/**
 * @file ArbolBinario.c
 * @brief Crea un árbol binario de búsqueda.
 * 
 * Este archivo contiene las funciones necesarias para la inserción y eliminación de un elemento del árbol.
 * También contiene las funciones para recorrer el árbol InOrder, PreOrder y PosOrder, así como la función para mostrar el árbol.
 * 
 * @author García Escamilla Bryan Alexis
 * @date 2025-10-21
 */

#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <stdbool.h>

#define VERSION "1.0"

typedef struct Node {
    int num;
    struct Node *left;
    struct Node *right;
    struct Node *father;
} Node;

// Punteros
Node *root = NULL; 

Node *CrearNodo(int num, Node *father);
void Insertar(Node **tree, int num, Node *father);
void MostrarArbol(Node *tree, int counter);
bool Buscar(Node *tree, int num);
void PreOrder(Node *tree);
void InOrder(Node *tree);
void PosOrder(Node *tree);
void Eliminar(Node *tree, int num);
void EliminarNodo(Node *delete);
Node *Minimo(Node *tree);
void Reemplazar(Node *tree, Node *new);
void DestruirNodo(Node *delete);

// Programa principal
int main(int argc, char const *argv[]) {
    int num, op = 0, counter = 0;

    do  {
        system("cls");
        printf("/*-----------------------------------.");
        printf("\n| PROGRAMA QUE CREA UN ARBOL BINARIO |");
        printf("\n`-----------------------------------*/");
        printf("\n\n>> Elija una de las opciones");
        printf("\n\n1.- Insertar un numero en el arbol");
        printf("\n2.- Mostrar arbol");
        printf("\n3.- Bucar un numero en el arbol");
        printf("\n4.- Recorrer el arbol en PreOrder");
        printf("\n5.- Recorrer el arbol en InOrder");
        printf("\n6.- Recorrer el arbol en PosOrder");
        printf("\n7.- Eliminar un numero del arbol");
        printf("\n8.- Salir del programa");
        printf("\n\nOpcion: ");
        scanf("%d", &op);

        switch (op) {
            case 1:
                printf("\n__INSERTAR UN NUMERO EN EL ARBOL__");
                printf("\n\nEscribe el numero a insertar: ");
                scanf("%d", &num);
                Insertar(&root, num, NULL);
                getch();
                break;
            case 2:
                printf("\n__MOSTRAR ARBOL__\n\n");
                MostrarArbol(root, counter);
                getch();
                break;
            case 3:
                printf("\n__BUSCAR UN NUMERO EN EL ARBOL__");
                printf("\n\nEscribe el numero a buscar: ");
                scanf("%d", &num);
                if (Buscar(root, num)) {
                    printf("\nEl numero %d si se encuentre en el arbol", num);
                } else { 
                    printf("\nEl numero %d no se encuentra en el arbol", num);
                }
                getch();
                break;
            case 4:
                printf("\n__RECORRIDO EN PRE-ORDER__");
                printf("\n\nRecorrido: ");
                PreOrder(root);
                getch();
                break;
            case 5:
                printf("\n__RECORRIDO EN IN-ORDER__");
                printf("\n\nRecorrido: ");
                InOrder(root);
                getch();
                break;
            case 6:
                printf("\n__RECORRIDO EN POS-ORDER__");
                printf("\n\nRecorrido: ");
                PosOrder(root);
                getch();
                break;
            case 7:
                printf("\n__ELIMINAR UN NUMERO DEL ARBOL__");
                printf("\n\nEscribe el numero a eliminar: ");
                scanf("%d", &num);
                Eliminar(root, num);
                getch();
                break;
            case 8:
                printf("\n>> Gracias por probar el programa, regrese pronto");
                getch();
                break;
            default:
                printf("\n>> ERORR: La opción no es valida");
                getch();
                break;
        }
    } while(op != 8);

    return 0;
}

/**
 * @brief Crea un nuevo nodo.
 * 
 * Esta función crea un nuevo nodo para después insertarlo en el árbol. Hace los enlaces
 * correspondientes para el lado derecho e izquierdo así como para el nodo padre.
 * 
 * @param num Número que contiene el nodo a crear.
 * @param father Puntero al padre del nodo a crear.
 * 
 * @return Nodo creado. 
 * 
 */
Node *CrearNodo(int num, Node *father) {
    Node *new = malloc(sizeof(Node)); // Se crea el nuevo nodo
    
    if (new == NULL) { // Se verifica si el nodo se creo correctamente
        printf("\n>> ERROR: Hubo un error al crear la lista");
        return NULL;
    }

    // Se hacen los enlaces
    new -> num = num;
    new -> left = NULL;
    new -> right = NULL;
    new -> father = father;
    return new;
}

/**
 * @brief Inserta un nodo en el árbol.
 * 
 * Esta función recursiva inserta un nuevo nodo en el árbol teniendo en
 * cuenta si su valor es mayor o menor al del nodo actual.
 * 
 * @param tree Puntero al puntero del nodo actual.
 * @param num Número que contiene el nodo a insertar.
 * @param father Puntero al padre del nodo a insertar.
 */
void Insertar(Node **tree, int num, Node *father) {
    if (*tree == NULL) { // Si el árbol esta vacío
        Node *new = CrearNodo(num, father);
        *tree = new;
    } else { // Si el árbol tiene un nodo o más
        int root_value = (*tree) -> num; // Obtenemos el valor de la raíz

        if (num < root_value) { // Se inserta el nodo a la izquierda
            Insertar(&(*tree) -> left, num, *tree);
        } else if (num > root_value) {
            Insertar(&(*tree) -> right, num, *tree);
        } else {
            return;
        }
    }
}

/**
 * @brief Imprimr el árbol de forma vertical.
 * 
 * Esta función recursiva primero muestra la rama derecha del árbol, luego la raíz
 * y finalmente la rama izquierda. Para representar la jerarquía del árbol
 * se usan espacios en blanco.
 * 
 * @param tree Puntero al nodo actual.
 * @param counter Contador para represesntar la jerarquía en el árbol.
 */
void MostrarArbol(Node *tree, int counter) {
    if (tree == NULL) { // Si el árbol esta vacío
        return;
    } else {
        // Imprimimos el árbol del lado derecho
        MostrarArbol(tree -> right, counter + 1);

        for (int i = 0; i < counter; i++) {
            printf("   ");
        }

        printf("%d\n", tree -> num);
        
        // Imprimimos el árbol del lado izquierdo
        MostrarArbol(tree -> left, counter + 1);
    }
}

/**
 * @brief Busca un nodo en el árbol.
 * 
 * Esta función recursiva busca un nodo en el árbol, teniendo en cuanta
 * si su valor es mayor o menor al de la raíz.
 * 
 * @param tree Puntero al nodo actual.
 * @param num Número a buscar en el árbol.
 * 
 * @return True si se ecuentra, False en caso contrario.
 */
bool Buscar(Node *tree, int num) {
    if (tree == NULL) { // Si el árbol esta vacío
        return false;
    } else if (tree -> num == num) {
        return true;
    } else if (num < tree -> num) {
        return Buscar(tree -> left, num);
    } else {
        return Buscar(tree -> right, num);
    }
}

/**
 * @brief Recorre el árbol en PreOrder.
 * 
 * Esta función recursiva, primero recorre la raíz, luego la rama izquierda
 * y finanmente la rama derecha.
 * 
 * @param tree Apuntador al nodo actual.
 */
void PreOrder(Node *tree) {
    if (tree == NULL) { // Si el árbol esta vacío
        return;
    } else {
        printf("[%d]", tree -> num);
        PreOrder(tree -> left);
        PreOrder(tree -> right);
    }
}

/**
 * @brief Recorre el árbol en InOrder.
 * 
 * Esta función recursiva, primero recorre la rama izquierda, luego la raíz
 * y finalmente la rama derecha.
 * 
 * @param tree Apuntador al nodo actual.
 */
void InOrder(Node *tree) {
    if (tree == NULL) { // Si el árbol esta vacío
        return;
    } else {
        InOrder(tree -> left);
        printf("[%d]", tree -> num);
        InOrder(tree -> right);
    }
}

/**
 * @brief Recorre al árbol en PosOrder.
 * 
 * Esta función recursiva, primero recorre la rama izquierda, luego la rama derecha
 * y finalmente la raíz.
 * 
 * @param tree Puntero al nodo actual.
 */
void PosOrder(Node *tree) {
    if (tree == NULL) { // Si el árbol esta vacío
        return;
    } else {
        PosOrder(tree -> left);
        PosOrder(tree -> right);
        printf("[%d]", tree -> num);
    }
}

/**
 * @brief Busca el nodo a eliminar del árbol.
 * 
 * Esta función recuriva busca el nodo a elimnar.
 * 
 * @param tree Puntero al nodo actual.
 * @param num Valor del nodo a eliminar.
 */
void Eliminar(Node *tree, int num) {
    if (tree == NULL) { // Si el árbol esta vacío
        return;
    } else if (num < tree -> num) {
        Eliminar(tree -> left, num);
    } else if (num > tree -> num) {
        Eliminar(tree -> right, num);
    } else { // Si ya encontraste el valor
        EliminarNodo(tree);
    }
}

/**
 * @brief Busca el nodo más a la izquierda posible.
 * 
 * @param tree Puntero al nodo actual.
 * 
 * @return Puntero al nodo más a la izquierda.
 */
Node *Minimo(Node *tree) {
    if (tree == NULL) { // Si el árbol esta vacío
        return NULL;
    }

    if (tree -> left) { // Si tiene hijo izquierdo
        return Minimo(tree -> left); // Buscamos la parte más izquierda posible
    } else {
        return tree;
    }
}

/**
 * @brief Reemplaza el nodo viejo por el nuevo.
 * 
 * Esta función reemplaza el nodo viejo por el nuevo, para asignar el
 * nodo padre e hijo correspondiente.
 * 
 * @param tree Puntero al nodo actual.
 * @param new Puntero al nodo nuevo, NULL si el nodo actual es hoja.
 */
void Reemplazar(Node *tree, Node *new) {
    if (tree -> father) { // Si el árbol tiene padre
        // Se le asigna a tree -> father su nuevo hijo
        if (tree == tree -> father -> left) { // Si el hijo es el izquierdo
            tree -> father -> left = new;   
        } else if (tree == tree -> father -> right) { // Si el hijo es el derecho
            tree -> father -> right = new;
        }
    }

    if (new) {
        // Se le asigna su nuevo hijo
        new -> father = tree -> father;
    }
}

/**
 * @brief Elimina un nodo.
 * 
 * Esta función elimina el nodo que ya no pertenece al árbol, ajustando sus enlaces.
 * 
 * @param node_delete Puntero al nodo a eliminar.
 */
void DestruirNodo(Node *node_delete) {
    node_delete -> left = NULL;
    node_delete -> right = NULL;
    node_delete -> father = NULL;

    free(node_delete);
}

/**
 * @brief Elimina un nodo del árbol.
 * 
 * Esta función recursiva elimina un nodo del árbol, teniendo en cuenta si este tiene
 * un hijo, dos hijos o no tiene.
 * 
 * @param node_delete Puntero al nodo a eliminar
 */
void EliminarNodo(Node *node_delete) {
    if (node_delete -> left && node_delete -> right) { // Si el nodo tiene dos hijos
        Node *minor = Minimo(node_delete -> right);
        node_delete -> num = minor -> num;
        EliminarNodo(minor);
    } else if (node_delete -> left) { // Si tiene hijo izquierdo
        Reemplazar(node_delete, node_delete -> left);
        DestruirNodo(node_delete);
    } else if (node_delete -> right) { // Si tiene hijo derecho
        Reemplazar(node_delete, node_delete -> right);
        DestruirNodo(node_delete);
    } else { // Si no tiene hijos
        Reemplazar(node_delete, NULL);
        DestruirNodo(node_delete);
    }
}