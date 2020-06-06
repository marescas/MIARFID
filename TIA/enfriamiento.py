import random
import math
import pandas as pd
import argparse
import time


def fitness(solucion, numeros, valorBuscado):
    """
    :param solucion: solucion sobre la que queremos obtener el fitness
    :return: fitness
    """

    res = numeros[0]
    for operacion, numero in zip(solucion, numeros[1:]):
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

    if res < 0:
        return 2**100
    return valorBuscado-res


def obtenerSucesores(solucion, numeros, valorBuscado):
    """
    :param solucion: solucion
    :return: lista de sucesores
    """
    misSucesores = []
    for i in range(0, len(solucion)):
        posible = solucion.copy()
        for j in range(0, 4):
            posible[i] = j
            fitnessvalor = fitness(posible, numeros, valorBuscado)
            if fitnessvalor < 2**100:
                misSucesores.append(posible.copy())

    return misSucesores


def convergencia(iteracion, solucion, numeros, valorBuscado):
    """
    :param iteracion: numero de iteraciones en un instante de tiempo t
    :param solucion: solucion obtenida en un instante t
    :return: Devuelve verdadero si se ha superado el número máximo de iteraciones
    o
    se ha encontrado el valor objetivo
    """
    return iteracion > 1000000 or fitness(solucion, numeros, valorBuscado) == 0


def obtenerSolucion(sucesores):
    return sucesores.pop(sucesores.index(random.choice(sucesores)))


def actualizarTemperatura(iteraciones, k, temperatura):

    return temperatura / (1 + k * temperatura)


def enfriamiento(solucionInicial, temperaturaInicial, k, numeros, valorBuscado):
    sucesores = obtenerSucesores(solucionInicial, numeros, valorBuscado)
    iteraciones = 0
    solucionActual = solucionInicial.copy()
    mejorSolucion = solucionActual.copy()
    temperatura = temperaturaInicial
    while len(sucesores) > 0 and not convergencia(iteraciones, solucionActual, numeros, valorBuscado):

        solucionNueva = obtenerSolucion(sucesores)
        incrementoFitness = fitness(
            solucionActual, numeros, valorBuscado) - fitness(solucionNueva, numeros, valorBuscado)
        if incrementoFitness > 0:
            solucionActual = solucionNueva.copy()
            sucesores = obtenerSucesores(solucionActual, numeros, valorBuscado)

            if fitness(solucionActual, numeros, valorBuscado) < fitness(mejorSolucion, numeros, valorBuscado):
                mejorSolucion = solucionActual.copy()
                print("mejor solucion encontrada en ", mejorSolucion,
                      fitness(mejorSolucion, numeros, valorBuscado))

        else:
            #print("valor", math.e ** (incrementoFitness / temperatura))
            if random.random() < math.e ** (incrementoFitness / temperatura):
                solucionActual = solucionNueva.copy()
                sucesores = obtenerSucesores(
                    solucionActual, numeros, valorBuscado)

        iteraciones += 1
        temperatura = actualizarTemperatura(iteraciones, k, temperatura)
    return mejorSolucion


def experimentos(solucionInicial, numeros, objetivo):
    datos = {"temperatura": [], "k": [], "experimento": [], "mejorFitness": []}
    for temperature in [1, 10, 100, 1000, 10000]:
        for k in [0.001, 0.01, 0.1, 1, 10]:
            for experimento in range(100):
                mejorSolucion = enfriamiento(
                    solucionInicial, temperature, k, numeros, objetivo)
                datos["temperatura"].append(temperature)
                datos["k"].append(k)
                datos["experimento"].append(experimento)
                datos["mejorFitness"].append(fitness(
                    mejorSolucion, numeros, objetivo))
                print("experimento %d" % experimento)
    resultadosDataFrame = pd.DataFrame(datos)
    resultadosDataFrame.to_pickle("exportEvaluacionEnfriamiento.pkl")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Solución al problema de la secuencia de números mediante Algoritmos Genéticos")
    parser.add_argument("--temperature", default=5000,
                        required=False, help="Valor de la temperatura", type=int)
    parser.add_argument("--kvalue", default=0.01,
                        required=False, help="valor de K", type=float)
    parser.add_argument("--casosPrueba",  default=None,
                        required=False, help="Dataframe con los casos de prueba", type=str)
    args = parser.parse_args()
    resultados = {"numeros": [], "objetivo": [],  "mejorValor": [], "time": []}
    if args.casosPrueba is not None:
        df = pd.read_pickle(args.casosPrueba)
    else:
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
    i = 0
    for index, row in df.iterrows():

        print("Numeros %s " % row["numeros"])
        print("Valor buscado %s" % row["objetivo"])
        #solucionInicial = [0]*(len(row["numeros"])-1)
        solucionesIniciales = [[0, 0, 2, 0, 0], [2, 0, 0, 2, 2], [2, 0, 1, 1, 1], [
            0, 1, 1, 1, 2], [2, 2, 2, 0, 1], [2, 0, 2, 1, 0], [0, 0, 0, 2, 1], [0, 2, 2, 0, 2], [0, 0, 1, 0, 2],
            [2, 2, 2, 1, 0], [2, 2, 1, 1, 1, 2, 0, 0, 1, 1, 2], [
                0, 2, 1, 1, 1, 1, 0, 2, 1, 0, 1],
            [1, 2, 0, 0, 0, 1, 0, 2, 0, 1, 2], [
                1, 0, 1, 0, 2, 0, 2, 2, 1, 2, 1],
            [1, 2, 1, 0, 0, 0, 0, 1, 2, 1, 2], [1, 0, 1, 0, 1, 0,
                                                0, 0, 1, 0, 0], [0, 1, 1, 0, 1, 0, 2, 1, 0, 0, 1],
            [0, 1, 2, 2, 0, 0, 0, 1, 2, 0, 1], [2, 1, 0, 1, 2, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 2, 2, 0, 1, 0, 0, 0]]
        start = time.time()
        mejorSolucion = enfriamiento(
            solucionesIniciales[i], args.temperature, args.kvalue, row["numeros"], row["objetivo"])
        end = time.time()
        resultados["objetivo"].append(row["objetivo"])
        resultados["numeros"].append(row["numeros"])
        resultados["time"].append(end-start)
        resultados["mejorValor"].append(
            row["objetivo"]-fitness(mejorSolucion, row["numeros"], row["objetivo"]))
        i += 1
        print("\n MejorSolucion: %s fitness: %s \n" % (mejorSolucion,
                                                       fitness(mejorSolucion, row["numeros"], row["objetivo"])))
    resultadosDataFrame = pd.DataFrame(resultados)
    resultadosDataFrame.to_pickle("exportEnfriamiento.pkl")
    # num = [5, 6, 10, 8, 8, 75, 8, 9, 6, 4, 1, 75]
    # obj = 1603
    # experimentos([0]*(len(num)-1), num, obj)
