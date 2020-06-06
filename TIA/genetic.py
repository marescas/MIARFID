
import numpy as np
import random
import pandas as pd


def iniciarPopulacho(tamañoIndividuo, numIndividuos):
    """
    inicia el pueblo
    :param tamañoIndividuo: tamaño del individuo
    :param numIndividuos: numero de individuos en la población
    :return pueblo:
    """
    pueblo = [list(np.random.randint(4, size=tamañoIndividuo))
              for _ in range(0, numIndividuos)]
    return pueblo


def aptitud(individuo, numeros, valorBuscado):
    """

    Evalua un individuo:
         No se arregla ningun individuo
         Si el resultado de la división es decimal --> Peor valor
         Si nos pasamos --> Peor valor
    :param individuo: individuo codificado
    0 --> suma
    1 --> resta
    2 --> multiplicacion
    3 --> division
    :param numeros: datos del problema
    :param valorBuscado: valor que queremos aproximar sin pasarnos
    """
    res = numeros[0]
    for operacion, numero in zip(individuo, numeros[1:]):
        if operacion == 0:
            res += numero
        if operacion == 1:
            res -= numero
        if operacion == 2:
            res *= numero
        if operacion == 3:
            res /= numero
            if type(res) == float:
                # El resultado de la division no puede ser decimal
                return 2**100
    if res > valorBuscado:
        # si me paso devuelvo un valor muy alto
        return 2**100
    return valorBuscado-res


def seleccion_elitista(pueblo, probCruce, numeros, valorBuscado):
    """
    Seleccionamos los individuos que se van a cruzar
    Aquellos que tengan un mejor fitness serán los escogidos para cruzarse
    :param pueblo: lista
    """
    preseleccion = []
    for individuo in pueblo:
        validez = aptitud(individuo, numeros, valorBuscado)
        preseleccion.append((individuo, validez))
    preseleccion = sorted(preseleccion, key=lambda tup: tup[1])
    seleccionados = [preseleccion[0][0], preseleccion[1][0]]
    return seleccionados


def seleccion_elitista_probCruce(pueblo, probCruce, numeros, valorBuscado):
    """
    Seleccionamos los individuos que se van a cruzar
    :param pueblo: lista
    """
    preseleccion = []
    for individuo in pueblo:
        validez = aptitud(individuo, numeros, valorBuscado)
        preseleccion.append((individuo, validez))
    preseleccion = sorted(preseleccion, key=lambda tup: tup[1])
    ix = 0
    seleccionados = []
    while True:
        if random.random() > 1-probCruce:
            seleccionados.append(preseleccion[ix][0])
        if len(seleccionados) == 2:
            return seleccionados
        if ix == len(preseleccion):
            ix = 0
        ix += 1


def seleccion(pueblo, probCruce, numeros, valorBuscado, modo="elitistaProbCruce"):
    if modo == "elitista":
        return seleccion_elitista(pueblo, probCruce, numeros, valorBuscado)
    elif modo == "elitistaProbCruce":
        return seleccion_elitista_probCruce(pueblo, probCruce, numeros, valorBuscado)


def cruce(seleccionados):
    hijos = []
    longitudIndividuo = len(seleccionados[0])
    hijos.append(seleccionados[0][0:int(
        longitudIndividuo/2)+1]+seleccionados[1][int(longitudIndividuo/2):-1])
    hijos.append(seleccionados[1][0:int(
        longitudIndividuo/2)+1]+seleccionados[0][int(longitudIndividuo/2):-1])
    return hijos


def mutacion(nuevaGeneracion, probMutacion):
    for individuo in nuevaGeneracion:
        ix = 0
        while ix < len(nuevaGeneracion):
            if random.random() > 1-probMutacion:
                individuo[ix] = random.randint(0, 3)
            ix += 1
    return nuevaGeneracion


def reemplazoConCompactacion(pueblo, nuevaGeneracion):
    nuevoPueblo = pueblo+nuevaGeneracion
    nuevoPuebloCompacto = list(set(tuple(element) for element in nuevoPueblo))
    nuevoPueblo = [list(element) for element in nuevoPuebloCompacto]
    return nuevoPueblo


def reemplazoSimple(pueblo, nuevaGeneracion):
    nuevoPueblo = pueblo+nuevaGeneracion
    return nuevoPueblo


def reemplazo(pueblo, nuevaGeneracion,  numeros, valorBuscado, modo="compactacion"):
    if modo == "simple":
        return reemplazoSimple(pueblo, nuevaGeneracion)
    if modo == "compactacion":
        return reemplazoConCompactacion(pueblo, nuevaGeneracion)


def convergencia(pueblo, numeros, valorBuscado):
    for individuo in pueblo:
        if aptitud(individuo, numeros, valorBuscado) == 0:
            return True, individuo
    return False, None


def mostrarResultados(individuos, numeros, valorBuscado):
    res = ""
    for individuo in individuos:
        res += str(numeros[0])
        resNumerico = numeros[0]
        for operacion, numero in zip(individuo, numeros[1:]):
            if operacion == 0:
                res += "+" + str(numero)
                resNumerico += numero
            if operacion == 1:
                res += "-" + str(numero)
                resNumerico -= numero
            if operacion == 2:
                res += "*" + str(numero)
                resNumerico *= numero
            if operacion == 3:
                res += "/" + str(numero)
                resNumerico /= numero

        res += "=%d  fitness: %s \n" % (resNumerico,
                                        aptitud(individuo, numeros, valorBuscado))

    print(res)


def genetico(maxIter, probCruce, probMutacion, numeros, valorBuscado, verbose=False):
    if verbose:
        print("Los numeros son: %s" % (str(numeros)))
        print("El valor buscado es: %s" % valorBuscado)
    iteracion = 0
    terminar = False
    pueblo = iniciarPopulacho(len(numeros)-1, len(numeros)*2)
    if verbose:
        print("Poblacion inicial: %s" % str(pueblo))
    while not terminar:
        seleccionados = seleccion(pueblo, probCruce, numeros, valorBuscado)
        if verbose:
            print("Individuos seleccionados: %s" % str(seleccionados))
        nuevaGeneracion = cruce(seleccionados)
        if verbose:
            print("Hijos: %s" % str(nuevaGeneracion))
        nuevaGeneracion = mutacion(nuevaGeneracion, probMutacion)
        if verbose:
            print("Hijos mutados: %s" % str(nuevaGeneracion))
        pueblo = reemplazo(pueblo, nuevaGeneracion, numeros, valorBuscado)
        if verbose:
            print("Nuevo pueblo: %s" % str(pueblo))
            print("Longitud del nuevo pueblo: %d" % len(pueblo))
        iteracion += 1
        converge = convergencia(pueblo, numeros, valorBuscado)
        terminar = iteracion > maxIter or converge[0]
    mostrarResultados(seleccion(pueblo, probCruce, numeros,
                                valorBuscado), numeros, valorBuscado)


if __name__ == "__main__":
    datos = {"numeros": [[4, 10, 7, 9, 2, 25],
                         [10, 2, 9, 5, 7, 100],
                         [2, 75, 9, 6, 100, 8],
                         [3, 10, 7, 6, 75, 10],
                         [7, 3, 50, 25, 6, 100],
                         [2, 4, 75, 4, 50, 2],
                         [9, 6, 75, 7, 2, 50]
                         ],
             "objetivo": [232, 298, 474, 381, 741, 502, 264]}
    df = pd.DataFrame(datos)
    for index, row in df.iterrows():
        print("Numeros %s " % row["numeros"])
        print("Valor buscado %s" % row["objetivo"])
        genetico(maxIter=100000, probCruce=0.5,  probMutacion=0.6, numeros=row["numeros"],
                 valorBuscado=row["objetivo"], verbose=True)
