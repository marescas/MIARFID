
import numpy as np
import random
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import time


def iniciarPopulacho(tamañoIndividuo, numIndividuos):
    """
    inicia el pueblo
    :param tamañoIndividuo: tamaño del individuo
    :param numIndividuos: numero de individuos en la población
    :return pueblo: set de tuplas (no repetidos)
    """
    pueblo = set(tuple(np.random.randint(4, size=tamañoIndividuo))
                 for _ in range(0, numIndividuos))
    return pueblo


def aptitudSinArreglo(individuo, numeros, valorBuscado):
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

    if res < 0:
        return 2**100
    return valorBuscado-res


def aptitud(individuo, numeros, valorBuscado, modo="sinArreglo"):
    return aptitudSinArreglo(individuo, numeros, valorBuscado)


def seleccion_elitista(pueblo, probCruce, numeros, valorBuscado):
    """
    Seleccionamos los individuos que se van a cruzar
    Aquellos que tengan un mejor fitness serán los escogidos para cruzarse
    :param seleccionados: lista con los padres
    """
    preseleccion = []
    for individuo in pueblo:
        validez = aptitud(individuo, numeros, valorBuscado)
        preseleccion.append((individuo, validez))
    preseleccion = sorted(preseleccion, key=lambda tup: tup[1])
    seleccionados = [list(preseleccion[0][0]), list(preseleccion[1][0])]
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
        if ix >= len(preseleccion)-1:
            ix = 0
        ix += 1


def seleccion(pueblo, probCruce, numeros, valorBuscado, modo="elitista"):
    if modo == "elitista":
        return seleccion_elitista(pueblo, probCruce, numeros, valorBuscado)
    else:
        return seleccion_elitista_probCruce(pueblo, probCruce, numeros, valorBuscado)


def crucePor1Punto(seleccionados):
    hijos = []
    longitudIndividuo = len(seleccionados[0])
    hijos.append(tuple(seleccionados[0][0:int(
        longitudIndividuo/2)+1]+seleccionados[1][int(longitudIndividuo/2):-1]))
    hijos.append(tuple(seleccionados[1][0:int(
        longitudIndividuo/2)+1]+seleccionados[0][int(longitudIndividuo/2):-1]))
    return hijos


def cruceUniforme(seleccionados):
    hijos = []
    longitudIndividuo = len(seleccionados[0])
    j = 0
    while j < 2:
        hijo = []
        for i in range(longitudIndividuo):
            if random.random() > 0.5:
                hijo.append(seleccionados[0][i])
            else:
                hijo.append(seleccionados[1][i])
        hijos.append(tuple(hijo))
        j += 1
    return hijos


def cruce(seleccionados, modo="uniforme"):
    if modo == "1punto":
        return crucePor1Punto(seleccionados)
    else:
        return cruceUniforme(seleccionados)


def mutacion(nuevaGeneracion, probMutacion):
    generacionMutada = []
    for individuo in nuevaGeneracion:
        ix = 0
        individuoLista = list(individuo)
        while ix < len(individuoLista):
            if random.random() > 1-probMutacion:
                individuoLista[ix] = random.randint(0, 3)
            ix += 1
        generacionMutada.append(tuple(individuoLista))
    #print("generacion mutada " + str(generacionMutada))
    return generacionMutada


def juicioFinal(pueblo, nuevaGeneracion, numeros, valorBuscado):
    nuevoPueblo = list(pueblo.union(set(nuevaGeneracion)))
    puebloOrdenado = sorted(
        nuevoPueblo, key=lambda t: aptitud(t, numeros, valorBuscado))
    pueblo = iniciarPopulacho(len(puebloOrdenado[0]), len(puebloOrdenado[0])*2)
    pueblo.add(puebloOrdenado[0])
    return pueblo


def estadoEstacionario(pueblo, nuevaGeneracion, numeros, valorBuscado):
    nuevoPueblo = list(pueblo.union(set(nuevaGeneracion)))
    longitudPueblo = len(nuevoPueblo)-len(pueblo)
    puebloOrdenado = sorted(
        nuevoPueblo, key=lambda t: aptitud(t, numeros, valorBuscado))
    return set(puebloOrdenado[0:-longitudPueblo]) if longitudPueblo > 0 else set(puebloOrdenado)


def reemplazo(pueblo, nuevaGeneracion,  numeros, valorBuscado, modo="estadoEstacionario"):
    if modo == "juicioFinal":
        return juicioFinal(pueblo, nuevaGeneracion, numeros, valorBuscado)
    else:
        return estadoEstacionario(pueblo, nuevaGeneracion, numeros, valorBuscado)


def convergencia(pueblo, numeros, valorBuscado):
    for individuo in pueblo:
        if aptitud(individuo, numeros, valorBuscado) == 0:
            return True, individuo
    return False, None


def mostrarResultados(individuos, numeros, valorBuscado):
    resultadosNumericos = []
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

        aptitudIndividuo = aptitud(individuo, numeros, valorBuscado)
        res += "=%d  fitness: %s \n" % (resNumerico, aptitudIndividuo)
        resultadosNumericos.append(resNumerico)

    if aptitud(individuos[0], numeros, valorBuscado) == 2**100:
        print("No se ha podido encontrar un resultado en las iteraciones propuestas")
    else:
        print(res)
        print(individuos[0])
    return resultadosNumericos


def estancado(valorIteracionAnterior, valorActual, contador):
    if valorIteracionAnterior == valorActual:
        return contador + 1
    else:
        return 0


def genetico(maxIter, probCruce, probMutacion, numeros, valorBuscado, args=None, verbose=False):
    valorPorIteracion = []
    if verbose:
        print("Los numeros son: %s" % (str(numeros)))
        print("El valor buscado es: %s" % valorBuscado)
    iteracion = 0
    terminar = False
    pueblo = iniciarPopulacho(len(numeros)-1, len(numeros)*2)
    if verbose:
        print("Poblacion inicial: %s" % str(pueblo))
    valorIteracionAnterior = 2**100
    contadorEstancado = 0
    while not terminar:
        seleccionados = seleccion(
            pueblo, probCruce, numeros, valorBuscado, modo=args.modoSeleccion)
        valorPorIteracion.append(
            valorBuscado-aptitud(seleccionados[0], numeros, valorBuscado))
        if verbose:
            print("Individuos seleccionados: %s" % str(seleccionados))
        nuevaGeneracion = cruce(seleccionados, modo=args.modoCruce)
        if verbose:
            print("Hijos: %s" % str(nuevaGeneracion))
        nuevaGeneracion = mutacion(nuevaGeneracion, probMutacion)
        if verbose:
            print("Hijos mutados: %s" % str(nuevaGeneracion))
        pueblo = reemplazo(pueblo, nuevaGeneracion, numeros,
                           valorBuscado, modo=args.modoRemplazo)
        if verbose:
            print("Nuevo pueblo: %s" % str(pueblo))
            print("Longitud del nuevo pueblo: %d" % len(pueblo))
        iteracion += 1
        converge = convergencia(pueblo, numeros, valorBuscado)
        valorActual = sorted(aptitud(individuo, numeros, valorBuscado)
                             for individuo in pueblo)[0]

        contadorEstancado = estancado(
            valorIteracionAnterior, valorActual, contadorEstancado)
        valorIteracionAnterior = valorActual
        terminar = iteracion > maxIter or converge[0] or (
            contadorEstancado > args.contadorEstanco and valorActual != 2**100)
    resultadosNumericos = mostrarResultados(seleccion(pueblo, probCruce, numeros,
                                                      valorBuscado), numeros, valorBuscado)
    return valorPorIteracion, resultadosNumericos, iteracion, contadorEstancado


def experimento(datos, args):
    resultados = {"Tipo seleccion": [], "Tipo cruce": [], "Tipo reemplazo": [], "valores": [], "mejorValor": [], "SegundoMejorValor": [], "objetivo": [],
                  "numeros": [], "probCruce": [], "probMutacion": [], "iteraciones": [], "contadorEstancado": [], "time": []}
    for seleccion in ["elitista", "ElististaConProb"]:
        for cruce in ["1punto", "uniforme"]:
            for reemplazo in ["estadoEstacionario", "juicioFinal"]:
                for probCruce in [0.4, 0.6, 0.8]:
                    for probMutacion in [0.025, 0.05, 0.075, 0.1]:
                        for index, row in datos.iterrows():
                            print("Numeros %s " % row["numeros"])
                            print("Valor buscado %s" % row["objetivo"])
                            args.modoRemplazo = reemplazo
                            args.modoSeleccion = seleccion
                            args.modoCruce = cruce
                            start = time.time()
                            valorPorIteracion, resultadosNumericos, iteraciones, contadorEstancado = genetico(maxIter=50000, probCruce=probCruce,  probMutacion=probMutacion, numeros=row["numeros"],
                                                                                                              valorBuscado=row["objetivo"], args=args, verbose=False)
                            end = time.time()
                            resultados["Tipo seleccion"].append(seleccion)
                            resultados["Tipo cruce"].append(cruce)
                            resultados["Tipo reemplazo"].append(reemplazo)
                            resultados["valores"].append(valorPorIteracion)
                            resultados["mejorValor"].append(
                                resultadosNumericos[0])
                            resultados["SegundoMejorValor"].append(
                                resultadosNumericos[1])
                            resultados["probCruce"].append(probCruce)
                            resultados["probMutacion"].append(probMutacion)
                            resultados["objetivo"].append(row["objetivo"])
                            resultados["numeros"].append(row["numeros"])
                            resultados["iteraciones"].append(iteraciones)
                            resultados["contadorEstancado"].append(
                                contadorEstancado)
                            resultados["time"].append(end-start)
    resultadosDataFrame = pd.DataFrame(resultados)
    resultadosDataFrame.to_pickle("exportExperimentoGenetico.pkl")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Solución al problema de la secuencia de números mediante Algoritmos Genéticos")
    parser.add_argument("--maxIter", default=50000,
                        required=False, help="numero máximo de iteraciones", type=int)
    parser.add_argument("--probCruce", default=0.8,
                        required=False, help="probabilidad de cruce", type=float)
    parser.add_argument("--probMutacion",
                        default=0.1, required=False, help="probabiliad de mutación", type=float)
    parser.add_argument("--verbose", default=False,
                        required=False, help="Modo Verbose", type=bool)
    parser.add_argument("--modoRemplazo", default="estadoEstacionario",
                        required=False, help="Modo de remplazo a utilizar estadoEstacionario o Juicio final", type=str)
    parser.add_argument("--modoSeleccion", default="elitista",
                        required=False, help="Modo de seleccion a utilizar elitista o elitista con probabilidad", type=str)
    parser.add_argument("--modoCruce",  default="1punto",
                        required=False, help="Modo de cruce a utilizar 1 punto o uniforme", type=str)
    parser.add_argument("--contadorEstanco",  default=10000,
                        required=False, help="Limite de iteraciones sin mejorar el fitness de una solucion", type=int)
    parser.add_argument("--casosPrueba",  default=None,
                        required=False, help="Dataframe con los casos de prueba", type=str)
    args = parser.parse_args()
    print("Parametros: " + str(args)+"\n")
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

    resultados = {"valores": [], "mejorValor": [], "SegundoMejorValor": [], "objetivo": [],
                  "numeros": [], "iteraciones": [], "contadorEstancado": [], "time": []}
    #experimento(df, args)
    for index, row in df.iterrows():
        print("Numeros %s " % row["numeros"])
        print("Valor buscado %s" % row["objetivo"])
        start = time.time()
        valorPorIteracion, resultadosNumericos, iteraciones, contadorEstancado = genetico(maxIter=args.maxIter, probCruce=args.probCruce,  probMutacion=args.probMutacion, numeros=row["numeros"],
                                                                                          valorBuscado=row["objetivo"], args=args, verbose=args.verbose)
        end = time.time()
        resultados["valores"].append(valorPorIteracion)
        resultados["mejorValor"].append(resultadosNumericos[0])
        resultados["SegundoMejorValor"].append(resultadosNumericos[1])
        resultados["objetivo"].append(row["objetivo"])
        resultados["numeros"].append(row["numeros"])
        resultados["iteraciones"].append(iteraciones)
        resultados["contadorEstancado"].append(contadorEstancado)
        resultados["time"].append(end-start)
    resultadosDataFrame = pd.DataFrame(resultados)
    resultadosDataFrame.to_pickle("export.pkl")
    print("Resultados exportados correctamente")
