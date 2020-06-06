import subprocess
import numpy as np
import math
import pandas as pd


def calculaPerplejidad(results):
    print("Perplejidades")
    dataframe = {"submodelo": [], "testSet": [], "perplejidad": []}
    for submodelo in results.keys():
        for testSet in results[submodelo]:
            perplejidad = 2 ** -(1 / 1000 * sum(math.log2(prob) for prob in results[submodelo][testSet] if prob > 0))
            print(submodelo, testSet, perplejidad)
            dataframe["submodelo"].append(submodelo)
            dataframe["testSet"].append(testSet)
            dataframe["perplejidad"].append(perplejidad.__round__(3))
    pd.DataFrame(dataframe).to_pickle("results.pkl")


def createConfusFile(data, testSetsName, outputFilename):
    f = ""
    for key in data.keys():
        for value in data[key]:
            f += "%s %s \n" % (key.split("-")[1], testSetsName[value[1]])
    output = open(outputFilename, "w")
    output.write(f)
    output.close()


if __name__ == '__main__':
    results = {}
    modelos = {"G1": ["G1-EQ", "G1-IS", "G1-SC"], "G2": ["G2-EQ", "G2-IS", "G2-SC"], "G3": ["G3-EQ", "G3-IS", "G3-SC"]}
    testSets = ["TS-EQ", "TS-IS", "TS-SC"]
    for modelo in modelos.keys():
        for submodelo in modelos[modelo]:
            for testSet in testSets:
                result = subprocess.check_output(
                    ["./scfg-toolkit/scfg_prob", "-g", "models/%s" % submodelo, "-m", "corpus/%s" % testSet])
                if results.get(submodelo) is None:
                    results[submodelo] = {testSet: np.array(result.decode('ascii').split("\n")[0:-1], dtype=np.float32)}
                else:
                    results[submodelo][testSet] = np.array(result.decode('ascii').split("\n")[0:-1], dtype=np.float32)

    maxProb = {}
    for modelo in modelos.keys():
        for testSet in testSets:
            i = 0
            probs = np.zeros((3, 1000))
            for submodelo in modelos[modelo]:
                probs[i] = results[submodelo][testSet]
                i += 1
                argMax = np.argmax(probs, axis=0)
                max = np.max(probs, axis=0)
                if maxProb.get(modelo) is None:
                    maxProb[modelo] = {testSet: list(zip(max, argMax))}
                else:
                    maxProb[modelo][testSet] = list(zip(max, argMax))
    calculaPerplejidad(results)
    for modelo in maxProb.keys():
        createConfusFile(maxProb[modelo], ["EQ", "IS", "SC"], modelo + ".out")
    print("Ficheros para la matriz de confusión generados")
