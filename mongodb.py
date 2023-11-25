import pymongo
import pandas as pd
import numpy as np

KEYWORDS = ["prabowo", "ganjar", "anies"]


def createConnection():
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["sentimen_analisis"]
    return db
    

def createTopic(title,amount,until,since):

    db = createConnection()

    total_data = db.topic.count_documents({})

    print(total_data)
    topic = {
        "topicId": total_data + 1,
        "title": title,
        "amount" : amount,
        "timeline" : {
            "until" : until,
            "since" : since
        }
    }

    db.topic.insert_one(topic)

    return total_data+1

def getAmount(topicId):
    db = createConnection()
    result = db.topic.find_one({"topicId": topicId}, {"amount": True})

    print(result['amount'])
    return result['amount']
  
  
def insertTweet(topicId):
    db = createConnection()
    
    for keyword in KEYWORDS:
        file_path = f'tweet-harvest/tweets-data/{topicId}_{keyword}_labelled.csv'

        # Membaca file CSV ke dalam DataFrame
        df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')
        
        tweet_data = df.to_dict(orient='records')

        # Update the document in the collection
        # Assuming 'topic' is your collection name
        # Assuming each document in the collection has a field 'tweets'
        # and 'topicId' to identify the document
        db.topic.update_one(
            {"topicId": topicId},
            {"$addToSet": {"tweets": {"$each": tweet_data}}},
            upsert=True
        )

    # Close the MongoDB connection
    db.client.close()
  
  
def menghitungSentimen(topicId):
    db = createConnection()
    
    jumlah_positif = []
    jumlah_negatif = []
    jumlah_netral = []
    
    for keyword in KEYWORDS:
        file_path = f'tweet-harvest/tweets-data/{topicId}_{keyword}_labelled.csv'

        # Membaca file CSV ke dalam DataFrame
        df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')

        # Menghitung berapa jumlah label yang bernilai "positif"
        positif = df['label'].value_counts().get('positif', 0)
        jumlah_positif.append(positif)

        # Menghitung berapa jumlah label yang bernilai "positif"
        negatif = df['label'].value_counts().get('negatif', 0)
        jumlah_negatif.append(negatif)

        # Menghitung berapa jumlah label yang bernilai "positif"
        netral = df['label'].value_counts().get('netral', 0)
        jumlah_netral.append(netral)

        # print(f"Jumlah Positif Prabowo : {jumlah_positif[0]}")
        # print(f"Jumlah Positif Ganjar : {jumlah_positif[1]}")
        # print(f"Jumlah Positif Anies : {jumlah_positif[2]}")
        # print("\n")
        # print(f"Jumlah Negatif Prabowo : {jumlah_negatif[0]}")
        # print(f"Jumlah Negatif Ganjar : {jumlah_negatif[1]}")
        # print(f"Jumlah Negatif Anies : {jumlah_negatif[2]}")
        # print("\n")
        # print(f"Jumlah Netral Prabowo : {jumlah_netral[0]}")
        # print(f"Jumlah Netral Ganjar : {jumlah_netral[1]}")
        # print(f"Jumlah Netral Anies : {jumlah_netral[2]}")
        
        print("panjang ", len(jumlah_positif))

    for i in range(3):
        jumlah_positif[i] = np.int64(jumlah_positif[i])  # Replace with the actual value
        jumlah_negatif[i] = np.int64(jumlah_negatif[i])  # Replace with the actual value
        jumlah_netral[i] = np.int64(jumlah_netral[i])  # Replace with the actual value

    # Convert int64 values to regular Python integers
    for i in range(3):
        jumlah_positif[i] = jumlah_positif[i].item()
        jumlah_negatif[i] = jumlah_negatif[i].item()
        jumlah_netral[i] = jumlah_netral[i].item()

    data_sentimen = {
        "sentiment" : {
            "prabowo": {"positif" : jumlah_positif[0], "negatif" : jumlah_negatif[0], "netral" : jumlah_netral[0]},
            "ganjar": {"positif" : jumlah_positif[1], "negatif" : jumlah_negatif[1], "netral" : jumlah_netral[1]},
            "anies": {"positif" : jumlah_positif[2], "negatif" : jumlah_negatif[2], "netral" : jumlah_netral[2]},
        }
    }
        
    db.topic.update_one({"topicId" : topicId}, {"$set": data_sentimen}, upsert=True)

#get data sentiment from mongodb
def get_sentiment_data():
    db = createConnection()    
    topics = db.topic.find({})

    sentiment_data = []

    for topic in topics:
        sentiment = topic.get("sentiment", {})

        data = {
            "topicId": topic["topicId"],
            "prabowo": sentiment.get("prabowo", {}),
            "ganjar": sentiment.get("ganjar", {}),
            "anies": sentiment.get("anies", {}),
        }

        sentiment_data.append(data)

    db.client.close()

    return sentiment_data
