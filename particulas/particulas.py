from .particula import Particula
import json
from .algoritmos import *

class Particulas:
    def __init__(self):
        self.__lista = []

    def agregarFinal(self, particula:Particula):
        self.__lista.append(particula)
    
    def agregarInicio(self, particula:Particula):
        self.__lista.insert(0, particula)
    
    def mostrar(self):
        for particula in self.__lista:
            print(particula)
    
    def __str__(self):
        return "".join(
            str(particula) + '\n' for particula in self.__lista
        )

    def __len__(self):
        return len(self.__lista)

    def __iter__(self):
        self.cont = 0
        return self
    
    def __next__(self):
        if self.cont < len(self.__lista):
            particula = self.__lista[self.cont]
            self.cont += 1
            return particula
        else: 
            raise StopIteration
    
    def guardar(self, ubicacion):
        try:
            with open(ubicacion, 'w') as archivo:
                lista = [particula.to_dict() for particula in self.__lista]
                json.dump(lista, archivo, indent=5)
            return 1
        except:
            return 0
    
    def abrir(self, ubicacion):
        try:
            with open(ubicacion, 'r') as archivo:
                lista = json.load(archivo)
                self.__lista = [Particula(**particula) for particula in lista]
            return 1
        except:
            return 0

    def sort_by_id(self):
        self.__lista.sort(key=lambda particula: particula.id)
    def sort_by_distancia(self):
        self.__lista.sort(key=lambda particula: particula.distancia, reverse=True )
    def sort_by_velocidad(self):
        self.__lista.sort(key=lambda particula: particula.velocidad)

    def to_dict(self):
        grafo = dict()
        for particula in self.__lista:
            #   Origen 
            key = (particula.origen_x, particula.origen_y)
            value = ((particula.destino_x, particula.destino_y), round(particula.distancia))
            if key in grafo:
                grafo[key].append(value)
            else:
                grafo[key] = [value]
            #   Destino
            key = (particula.destino_x, particula.destino_y)
            value = ((particula.origen_x, particula.origen_y), round(particula.distancia))
            if key in grafo:
                grafo[key].append(value)
            else:
                grafo[key] = [value]

        self.grafo = grafo
        return self.grafo

    def to_dict_velocidad(self):
        grafo = dict()
        for particula in self.__lista:
            #   Origen 
            key = (particula.origen_x, particula.origen_y)
            value = ((particula.destino_x, particula.destino_y), round(particula.velocidad))
            if key in grafo:
                grafo[key].append(value)
            else:
                grafo[key] = [value]
            #   Destino
            key = (particula.destino_x, particula.destino_y)
            value = ((particula.origen_x, particula.origen_y), round(particula.velocidad))
            if key in grafo:
                grafo[key].append(value)
            else:
                grafo[key] = [value]

        self.grafo = grafo
        return self.grafo
        

    def recorrido_profundidad(self, origen):
        recorrido = recorridoProfundidad(self.grafo, origen)
        return self.recorrido_toString(recorrido)

    def recorrido_amplitud(self, origen):
        recorrido = recorridoAmplitud(self.grafo, origen)
        return self.recorrido_toString(recorrido)

    def recorrido_toString(self, recorrido):
        texto = ""
        for nodo in recorrido:
            texto += str(nodo) + "\n"
        return texto
    
    def prim(self, origen):
        return algoritmoPrim(self.grafo, origen)

    def kruskal(self):
        dict_grafo = self.to_dict_velocidad()
        return kruskal(dict_grafo)



#p01 = Particula(id=1, origen_x=150, origen_y=150, destino_x=500, destino_y=500, velocidad=300,
#                red=255, green=255, blue=255)
#p02 = Particula(id=2, origen_x=100, origen_y=100, destino_x=400, destino_y=400, velocidad=100,
#                red=0, green=0, blue=0)

# particulas = Particulas()
#particulas.agregarFinal(p01)
#particulas.agregarInicio(p02)
#particulas.agregarInicio(p01)
#particulas.mostrar()

