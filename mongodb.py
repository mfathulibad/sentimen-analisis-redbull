import pymongo
import pandas as pd
import numpy as np
import json
from datetime import datetime 

KEYWORDS = ["prabowo", "ganjar", "anies"]


def createConnection():
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["sentimen_analisis"]
    return db
    

def createTopic(title, amount, until, since):

    db = createConnection()

    # Mencari topicId terbesar
    last_topic = db.topic.find_one(sort=[("topicId", -1)])
    last_topic_id = last_topic["topicId"] if last_topic else 0

    topic = {
        "topicId": last_topic_id + 1,
        "title": title,
        "amount": amount,
        "timeline": {
            "until": until,
            "since": since
        }
    }

    db.topic.insert_one(topic)

    return last_topic_id + 1

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

def get_all_topics():
    db = createConnection()
    topics = db.topic.find({})
    topic_list = []

    for topic in topics:
        topic_data = {
            "topicId": topic["topicId"],
            "title": topic["title"],
            "amount": topic["amount"],
            "since": topic["timeline"]["since"],
            "until": topic["timeline"]["until"],
            "created_at": topic.get("created_at", ""),  # Add this line to get the created_at field
        }
        topic_list.append(topic_data)

    db.client.close()

    return topic_list

def delete_topic(topic_id):
    try:
        db = createConnection()
        db.topic.delete_one({"topicId": topic_id})
        print("BISA?: ", topic_id)
        print("Type of topic_id:", type(topic_id))
    except Exception as e:
        print(f"Error deleting topic: {e}")
    finally:
        db.client.close()
        

def peak_time(topicId):

    # Membuat koneksi ke database MongoDB
    db = createConnection()

    # Aggregation pipeline
    pipeline = [
        {
            "$match": {
                "topicId": topicId
            }
        },
        {"$unwind": "$tweets"},
        {
            "$project": {
                "keyword": "$tweets.keyword",
                "created_at": {
                    "$dateFromString": {
                        "dateString": {
                            "$dateToString": {
                                "format": "%Y-%m-%dT%H:%M:%S",
                                "date": {
                                    "$dateFromString": {
                                        "dateString": "$tweets.created_at",
                                        "format": "%Y-%m-%d %H:%M:%S%z"
                                    }
                                }
                            }
                        },
                        "format": "%Y-%m-%dT%H:%M:%S"
                    }
                }
            }
        },
        {
            "$group": {
                "_id": {
                    "keyword": "$keyword",
                    "day": {"$dayOfMonth": "$created_at"},
                    "month": {"$month": "$created_at"},
                    "year": {"$year": "$created_at"}
                },
                "count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "_id": 0,
                "keyword": "$_id.keyword",
                "date": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": {
                            "$dateFromParts": {
                                "year": "$_id.year",
                                "month": "$_id.month",
                                "day": "$_id.day"
                            }
                        }
                    }
                },
                "count": 1
            }
        }
    ]

    # Menjalankan aggregation
    result = list(db.topic.aggregate(pipeline))

    data = []
    # Menampilkan hasil
    for doc in result:
        data.append(doc)
    
    db.client.close()
    
    return data


def getTweets(topicId):
    db = createConnection()

    labels = ["positif", "negatif", "netral"]
    top_5_tweets_by_label = {}
    top_5_general_tweets = []

    for label in labels:
        pipeline = [
            {"$match": {"topicId": topicId, "tweets.label": label}},
            {"$unwind": "$tweets"},
            {"$match": {"tweets.label": label}},
            {"$sort": {
                "tweets.quote_count": -1,
                "tweets.reply_count": -1,
                "tweets.retweet_count": -1,
                "tweets.favorite_count": -1
            }},
            {"$group": {
                "_id": "$_id",
                "tweets": {"$push": "$tweets"}
            }},
            {"$project": {
                "top_tweets": {"$slice": ["$tweets", 5]}
            }}
        ]

        result = list(db.topic.aggregate(pipeline))

        if result:
            top_5_tweets_by_label[label] = result[0]['top_tweets']
            top_5_general_tweets.extend(result[0]['top_tweets'])

    # Menghilangkan duplikat dari top 5 tweets secara umum menggunakan id_str
    top_5_general_tweets_dict = {tweet['id_str']: tweet for tweet in top_5_general_tweets}
    top_5_general_tweets = list(top_5_general_tweets_dict.values())

    # Mengurutkan dan mengambil 5 tweets teratas secara umum
    top_5_general_tweets = sorted(top_5_general_tweets, key=lambda x: x['quote_count'] + x['reply_count'] + x['retweet_count'] + x['favorite_count'], reverse=True)[:5]

    # Format data top 5 tweets untuk masing-masing label dan secara umum ke dalam JSON
    data = {
        "general": top_5_general_tweets,
        "by_label": top_5_tweets_by_label
    }

    top_5_tweets_json = json.dumps(data, indent=4)  # Konversi ke JSON dengan indentasi untuk kejelasan
    
    print(top_5_tweets_json)

    db.client.close()
    
    return top_5_tweets_json