
import pymongo

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

    # db.topic.insert_one(topic)

    return topic.id_topic

createTopic("November Minggu Ke 1","500","2023-11-07","2023-11-03")