# -*- coding: utf-8 -*-
import math

import numpy as np
from sys import *
from distances import get_distance_matrix
from matplotlib.pyplot import matshow, show, cm, plot
import scipy
import logging


class qa:

    def __init__(self, total, long, origen, densidad):
        """

        :param total:
        :param long:
        :param origen:
        :param densidad:
        """
        self.total = total
        self.long = long
        self.origen = origen
        self.densidad = densidad


def lee_fichero(fichero):
    matriz = []
    fichero = open(fichero, "r")
    lineas = fichero.readlines()
    matriz = [linea.split() for linea in lineas]
    fichero.close()
    return np.array(matriz).astype(np.float)


# Implementar a partir de aqui
# sintaxis get_distance_matrix:
# distancias=get_distance_matrix(npmatriz1,npmatriz2,'cos')
# donde npmatriz1 y npmatriz2 son los vectores de características de los dos audios
def PD(distancias):
    M = {}
    maxi, maxj = distancias.shape
    for j in range(0, maxj):
        M[(0, j)] = qa(total=distancias[0, j], origen=j, long=1, densidad=distancias[0, j])
    for i in range(1, maxi):
        M[(i, 0)] = qa(total=distancias[i, 0] + M[(i - 1, 0)].total, origen=0, long=i,
                       densidad=(distancias[i, 0] + M[(i - 1, 0)].total) / i)
    for i in range(1, maxi):
        for j in range(1, maxj):
            lista = [(M[(i - 1, j)].total + distancias[i, j]) / (M[(i - 1, j)].long + 1),
                     (M[(i, j - 1)].total + distancias[i, j]) / (M[(i, j - 1)].long + 1),
                     (M[(i - 1, j - 1)].total + distancias[i, j]) / (
                             M[(i - 1, j - 1)].long + 1)]
            valor_minimo = distancias[i, j] + min(lista)
            posicion_minima = lista.index(min(lista))
            mipos = None
            if posicion_minima == 0:
                mipos = M[(i - 1, j)].origen
            elif posicion_minima == 1:
                mipos = M[(i, j - 1)].origen
            if posicion_minima == 2:
                mipos = M[(i - 1, j - 1)].origen

            M[(i, j)] = qa(total=valor_minimo, origen=mipos, long=i, densidad=valor_minimo / i)
    return M


def otrosMinimos(totales, valorMinimo, distanciaEntreMinimos):
    finMinimo = totales.index(valorMinimo)
    posiblesres = []
    for idx,item in enumerate(totales):
        if abs(finMinimo - idx) > distanciaEntreMinimos:
            fin = idx
            origen = pd[(distancias.shape[0] - 1, fin)].origen
            posiblesres.append((origen,fin,item))
    return min(posiblesres,key= lambda t:t[2])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    npmatrix1 = lee_fichero("mfc_queries/SEG-0062.mfc.raw")
    npmatrix2 = lee_fichero("largo250000.mfc.raw")
    distancias = get_distance_matrix(npmatrix1, npmatrix2, 'cos')
    logging.info("Lectura correcta")
    pd = PD(distancias)
    logging.info("Matriz computada correctamente")

    totales = [pd[(distancias.shape[0] - 1, j)].total for j in range(0, distancias.shape[1])]
    valorMinimo = min(totales)
    fin = totales.index(valorMinimo)
    origen = pd[(distancias.shape[0] - 1, fin)].origen
    print("origen %s, fin %s, valor minimo %.3f" % (origen, fin, valorMinimo))
    origen, fin, valorMinimo = otrosMinimos(totales, valorMinimo, 5)
    print("otroMinimo origen %s, fin %s, valor minimo %.3f" % (origen, fin, valorMinimo))
