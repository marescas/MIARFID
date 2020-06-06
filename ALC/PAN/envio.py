import os
import pandas as pd
import xml.etree.ElementTree as et
import argparse
import logging
import pickle
import sklearn
import warnings
import shutil

warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)


def read_data(path: str):
    """
    this method get the dataframes for the spanish and the english
    :param path: path to the inputDirectory
    :return: [dataFrameEn,DataFrameES]
    """

    langs = ["en", "es"]
    results = []
    for lang in langs:
        logger.warning("Create dataframe for lang %s" % lang)
        dataFrame = {"author": [], "tweets": []}
        pathEn = os.path.join(path, lang)

        for filename in os.listdir(pathEn):
            if filename != 'truth.txt' and  filename != ".DS_Store":
                xtree = et.parse(os.path.join(pathEn, filename))
                documents = xtree.getroot()[0]
                authorTweets = []
                for doc in documents.findall("document"):
                    authorTweets.append(doc.text)
            dataFrame["author"].append(filename.split(".")[0])
            dataFrame["tweets"].append(authorTweets)
        dataFrame = pd.DataFrame(dataFrame)
        dataFrame["tweetsClean"] = [" #finTweet# ".join(tweets) for tweets in list(dataFrame.tweets)]
        results.append(dataFrame)

    return results[0], results[1]


def classify(modelPath: str, dataframe: pd.DataFrame):
    """

    :param modelPath:
    :param dataframe:
    :return: [(id,label)]
    """
    # Load the model
    model = pickle.load(open(modelPath, 'rb'))
    # Get the predictions
    predictions = model.predict(dataframe.tweetsClean)
    # save the predictions in format
    res = list(zip(dataframe.author, predictions))
    return res


def save_to_xml(predictions: list, lang: str, outputDir: str):
    logger.warning("save predictions for language %s" % lang)
    path = "%s/%s" % (outputDir, lang)
    os.mkdir(path)
    for prediction in predictions:
        root = et.Element("author")
        root.set("id", prediction[0])
        root.set("lang", lang)
        root.set("type", str(prediction[1]))
        tree = et.ElementTree(root)
        tree.write(os.path.join(path, "%s.xml" % prediction[0]))


if __name__ == '__main__':
    logger = logging.getLogger("David + Marcos submission")
    parser = argparse.ArgumentParser("Marcos & David first Submission")
    parser.add_argument("-i", type=str, dest="inputDirectory", required=True, help="path to the input directory")
    parser.add_argument("-o", type=str, dest="outputDirectory", required=True, help="path to the output directory")
    args = parser.parse_args()
    dataFrameEN, dataFrameES = read_data(args.inputDirectory)
    logger.warning("Classify Spanish")
    listClassifyES = classify("esmodel.pkl", dataFrameES)
    logger.warning("Classify English")
    listClassifyEN = classify("enmodel.pkl", dataFrameEN)
    shutil.rmtree(args.outputDirectory, ignore_errors=True, onerror=None)
    os.mkdir(args.outputDirectory)
    save_to_xml(listClassifyES, "es", args.outputDirectory)
    save_to_xml(listClassifyEN, "en", args.outputDirectory)
