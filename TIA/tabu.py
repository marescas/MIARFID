import numpy as np
import itertools


def cacularMejorIndividuo(sol, numeros):
    elementosOrdenados = sorted(
        sol, key=lambda tup: fitness(tup, numeros))
    print(elementosOrdenados[0])
    return elementosOrdenados[0]


def calculaSucesores(sol):
    perm = itertools.permutations(list(sol))
    return set(perm)


def actualizarTabu(tabu, sol):
    print(tabu, sol)
    if len(tabu) < 12:
        nuevaTabu = list(tabu.copy()) + sol
    else:
        nuevaTabu = list(tabu.copy()[0:12])+sol
    return nuevaTabu


def fitness(sol, numeros):
    i = 0
    j = 1
    res = 0
    for _ in range(0, len(sol)-1):
        res += numeros[sol[i]][sol[j]]
        i += 1
        j += 1
    return res


def busqueda_tabu(sol_inicial, matrizDatos, tamañoTabu):
    tabu = []
    k = 0
    sol = sol_inicial.copy()
    mejor_solucion = sol_inicial.copy()
    acabar = False
    while k < 5000 and not acabar:
        k += 1
        sucesores = calculaSucesores(sol)
        if len(sucesores.difference(set(tabu))) == 0:
            acabar = True
        else:
            sol = cacularMejorIndividuo(
                sucesores.difference(set(tabu)), matrizDatos)
        if fitness(sol, matrizDatos) > fitness(mejor_solucion, matrizDatos):
            mejor_solucion = sol.copy()
        tabu = actualizarTabu(tabu, sol)
    return mejor_solucion


if __name__ == "__main__":
    datos = [[0, 10, 15, 25, 32],
             [41, 0, 57, 24, 52],
             [21, 31, 0, 21, 21],
             [66, 22, 15, 0, 47],
             [21, 44, 61, 47, 0]]
    sol_inicial = [0, 3, 4, 1, 2]
    print(busqueda_tabu(sol_inicial, datos, 12))
    print(fitness(sol_inicial, datos))
    print(calculaSucesores(sol_inicial))
