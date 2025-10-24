#include <stdio.h>
#include "matematica.h"

int main(int argc, char const *argv[]) {
    int a = 5, b = 9;

    printf("Suma: %d\n", sumar(a, b));
    printf("Resta: %d\n", resta(a, b));
    printf("Cuadrado de %d: %d\n", cuadrado(a));


    return 0;
}
