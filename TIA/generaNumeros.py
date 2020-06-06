import pandas as pd
import random
if __name__ == "__main__":
    datos = {"numeros": [], "objetivo": []}
    posiblesNumeros = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6,
                       6, 7, 7, 8, 8, 9, 9, 10, 10, 25, 50, 75, 100]
    print("Generando casos complicados")
    longitudOriginal = 6
    longitud = longitudOriginal
    for i in range(2, 4):
        print(i)
        for __ in range(10):
            datos["numeros"].append(
                [random.choice(posiblesNumeros) for _ in range(longitud)])
            datos["objetivo"].append(random.randint(
                int(longitud*101/6), int(longitud*999/6)))
        longitud = longitudOriginal * i
        print(longitud)
    df = pd.DataFrame(datos)
    print(df)
    df.to_pickle("./casos.pkl")
