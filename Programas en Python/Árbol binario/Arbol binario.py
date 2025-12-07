from Nodo import Nodo

class ArbolBinario:
    def __init__(self) -> None:
        self.raiz = None

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self.insertar_ref(self.raiz, valor)

    def insertar_ref(self, nodo, valor):
        if valor > nodo.valor:
            if nodo.derecha is None:
                nodo.derecha = Nodo(valor)
            else:
                self.insertar_ref(nodo.derecha, valor)
        else:
            if nodo.izquierda is None:
                nodo.izquierda = Nodo(valor)
            else:
                self.insertar_ref(nodo.izquierda, valor)

    