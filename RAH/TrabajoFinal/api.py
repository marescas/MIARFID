from wsgiref import simple_server

import falcon
import tweepy
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
from geopy.geocoders import Nominatim
import re
clean_re = re.compile('\W+')
url_re = re.compile("https?://[^\s]+")
hashtag_re = re.compile("#(\w+)")
mention_re = re.compile("@(\w+)")


def preprocessing(text):
    """
    Realiza el preprocesado de un determinado texto:
    1- sustituye las urls por la palabra <url>
    2- sustituye los hashtags por la palabra <hashtag>
    3- sustituye las menciones por la palabra <mencion>
    4- sustituye los numeros por la palabra <numero>
    """
    text = str(text)
    text_clean = url_re.sub("<url>", text)
    text_clean = hashtag_re.sub("<hashtag>", text_clean)
    text_clean = mention_re.sub("<mencion>", text_clean)
    text_clean = re.sub("\d+", "<numero>", text_clean)
    # text_clean = clean_re.sub(" ",text_clean).lower()
    text_clean = text_clean.lower()
    # text_clean = Stemming(text_clean)

    return text_clean

class RecuperaTweets:
    def __init__(self,ourTwitterAPI,modelLogistic,vectorizerBOW,geolocator):
        self.api  = ourTwitterAPI
        self.model = modelLogistic
        self.vectorizer = vectorizerBOW
        self.geocoder = geolocator
    def on_post(self,req,resp):
        requestDict = dict(req.media["queryResult"]["outputContexts"][0]["parameters"])
        print(requestDict)
        tweets = None
        msg = ""
        if requestDict.get("usuario"):
            #El usuario quiere leer tweets de un usuario
            tweets = api.user_timeline(screen_name=requestDict["usuario"][1:])
            msg = "Hemos conseguido recuperar %d tweets del usuario %s." % (len(tweets), requestDict["usuario"])
        if requestDict.get("hashtag"):
            # El usuario quiere leer tweets de un hashtag
            tweets = list(tweepy.Cursor(api.search,q=requestDict["hashtag"],count=100).items())
            msg = "Hemos conseguido recuperar %d tweets con el hashtag %s." % (len(tweets), requestDict["hashtag"])
        #public_tweets = self.api.home_timeline()
        if "solicitudanalizar" in req.media["queryResult"]["outputContexts"][0]["name"]:
            # El usuario quiere analizar el sentimiento de los tweets de un usuario o un hashtag
            tweetsPreprocessed = list(map(preprocessing, [tweet.text for tweet in tweets]))
            bowClasificar = self.vectorizer.transform(tweetsPreprocessed)
            prediccion = list(self.model.predict(bowClasificar))
            neutrales = prediccion.count("NEU")
            positivos = prediccion.count("P")
            negativos = prediccion.count("N")
            total = positivos+negativos+neutrales
            msg += "Tras el análisis concluimos que el %.2f es positivo y %.2f es negativo y %.2f es neutro" %(positivos/total*100,
                                                                                                               negativos/total*100,
                                                                                                      neutrales/total * 100)
        else:
            if requestDict.get("mylocation"):
                #El usuario quiere saber las tendencias en twitter para una localización especifica
                location = self.geocoder.geocode(requestDict.get("mylocation"))
                results = api.trends_closest(location.latitude, location.longitude)
                print(results)
                trends = api.trends_place(results[0]["woeid"])
                trendsJson = json.loads(json.dumps(trends, indent=1))
                for trend in trendsJson[0]["trends"]:
                    msg += trend["name"]+" "
            else:
                msg += "\nTe mostramos un par de ejemplos:"
                msg += "\n".join([tweet.text for tweet in tweets][:2])

        resp.body =json.dumps({'fulfillmentText': msg })



if __name__ == '__main__':
    auth = tweepy.OAuthHandler("xxxxxxx", "xxxxxxx")
    auth.set_access_token("xx-xx", "xx")

    api = tweepy.API(auth)


    app = falcon.API()
    geolocator = Nominatim(user_agent="localizador")
    modelLogistic = pickle.load(open("model.sav", 'rb'))
    vectorizer = pickle.load(open("vectorizer_model.sav", 'rb'))
    collectTweets = RecuperaTweets(api,modelLogistic,vectorizer,geolocator)
    app.add_route('/getTweets', collectTweets)
    print("Listo")
    httpd = simple_server.make_server('0.0.0.0', 8042, app)
    httpd.serve_forever()

