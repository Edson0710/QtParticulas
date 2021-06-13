import math
from queue import PriorityQueue

#   Algoritmo distancia euclidiana
def distancia_euclidiana(x1, y1, x2, y2):
    return math.sqrt(pow(x2-x1,2) + pow(y2-y1,2))

#   Algoritmo Recorrer el grafo en profundidad
def recorridoProfundidad(grafo:dict, origen):
    pila = []
    visitados = []
    recorrido = []

    pila.append(origen)
    visitados.append(origen)

    while pila:
        vertice = pila.pop()
        recorrido.append(vertice)
        adyacentes = grafo.get(vertice)
        for n in adyacentes:
            n = n[0]
            if n not in visitados:
                visitados.append(n)
                pila.append(n)
    return recorrido

#   Algoritmo Recorrer el grafo en amplitud
def recorridoAmplitud(grafo:dict, origen):
    cola = []
    visitados = []
    recorrido = []

    cola.append(origen)
    visitados.append(origen)

    while cola:
        vertice = cola[0]
        cola.pop(0)
        recorrido.append(vertice)
        adyacentes = grafo.get(vertice)
        for n in adyacentes:
            n = n[0]
            if n not in visitados:
                visitados.append(n)
                cola.append(n)
    return recorrido

#   Algoritmo de Prim 
def algoritmoPrim(grafo : dict, origen):
    pq = PriorityQueue()
    recorridos = []
    arbol = [] 
    recorridos.append(origen)

    for adyacentes in grafo.get(origen):
        arista = (adyacentes[1], origen, adyacentes[0])
        pq.put(arista)
    while not pq.empty():
        arista = pq.get()
        destino = arista[2]
        if destino not in recorridos:
            recorridos.append(destino)
            for adyacentes in grafo.get(destino):
                if adyacentes[0] not in recorridos:
                    adyacente = (adyacentes[1], destino, adyacentes[0])
                    pq.put(adyacente)
            arbol.append(arista)
    return arbol

#   Algoritmo de kruskal

class DisjointSet:
    def __init__(self):
        self.elements = []

    def print(self):
        print(self.elements)

    def make_set(self,element):
        for elem in self.elements:
            if element in elem:
                return False
        self.elements.append([element])
        return True

    def find_set(self,element):
        for index,elem in enumerate(self.elements):
            if element in elem:
                return index
        return -1 
    
    def union(self,A,B):
        index_A = self.find_set(A)
        index_B = self.find_set(B)

        self.elements[index_A] += self.elements[index_B]
        self.elements.pop(index_B)

def kruskal(grafo : dict):
    arbol_expansion = []
    ds = DisjointSet()
    lista = PriorityQueue()

    for nodo in grafo:
        for ady in grafo.get(nodo):
            arista = (ady[1] * - 1 , nodo, ady[0])     
            lista.put(arista)

        ds.make_set(nodo)

    ds.print()

    while not lista.empty():
        arista = lista.get()

        origen = arista[1]
        destino = arista[2]

        if ds.find_set(origen) != ds.find_set(destino):
            arbol_expansion.append(arista)
            ds.union(origen,destino)

            print(f"Arista = {arista}")    
            ds.print()

    return arbol_expansion

