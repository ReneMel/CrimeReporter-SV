# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import tweepy
import pandas as pd
from wit import Wit
import copy
import json
from csv import writer


# Esta es la funcion basica con la que se extrae cada Tweet.
def printtweetdata(n, ith_tweet):
    print()
    print(f"Tweet {n}:")
    print(f"Username:{ith_tweet[0]}")
    print(f"Tweet Text:{ith_tweet[1]}")
    print(f"Hashtags Used:{ith_tweet[2]}")

# Esta es la funcion con la que el bot procesa la data en un archivo .Json
def processdatawit(n, ith_tweet):


    try:
         print(f"Tweet {n}:")
         witre= Witcli.message(ith_tweet)
         print(str(witre))
         write_json(witre)
    except:
         print("Error, no detecta wit.ai el archivo.")


# Esta es la funcion con la que se crea CSV en el cual se va a leer ya la informacion.
def write_json(json_resp,filename='location_wit.csv'):
        location_tw =pd.DataFrame(columns=[
             'location', 'info'
        ])
        json_ent=json_resp['entities']
        print("data=" + str(json_ent['wit$location:location']));
        for item in json_ent['wit$location:location']:
            print("localizacion: "+item['body'])
            #text = json_resp['text']
            location = item['body']
            info = str(json_ent['wit$location:location'])

            ith_data=[ location, info]
            append_list_as_row(filename, ith_data)
            #location_tw.loc[len(location_tw)] = ith_data
            #location_tw.to_csv(filename)

# Esta es la funcion con la que se escriben registros en el CSV
def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)



# Extraer data haciendo uso de la API
def scrape( numtweet):
    # Crear un dataframe con pandas
    user_id="ultimahsv"
    search_terms = "#SeguridadCiudadana AND ultimahsv"
    date_since= "2019-01-01"
    db = pd.DataFrame(columns=['username',
                               'text',
                               'hashtags'])

    # Usando .cursor, funcionalidad de tweepy
    # esta tiene todos los componentes que se solicitarán.
    # se solicita la cantidad de tweets
    tweets = tweepy.Cursor(api.search_tweets,
                           #screen_name=user_id,
                           q=search_terms,#+" -filter:retweets",
                           #ince_id=date_since,
                           tweet_mode='extended').items(numtweet)


    list_tweets = [tweet for tweet in tweets]

    i = 1

    for tweet in list_tweets:
        username = tweet.user.screen_name
        hashtags = tweet.entities['hashtags']

        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:
            text = tweet.full_text
        hashtext = list()
        for j in range(0, len(hashtags)):
            hashtext.append(hashtags[j]['text'])

        ith_tweet = [username,  text, hashtext]
        db.loc[len(db)] = ith_tweet
        printtweetdata(i, ith_tweet)
        processdatawit(i,ith_tweet[1])
        i = i + 1
    filename = 'scraped_tweets.csv'

    #db.drop_duplicates()
    db.to_csv(filename)

# Esta es la funcion main.
if __name__ == '__main__':
#aca llaves keys, falta agrregar .env



    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth)

    numtweet = 1000

    scrape(numtweet)
    print('Scraping has completed!')

