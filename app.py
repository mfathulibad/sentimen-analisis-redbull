from flask import Flask, redirect, render_template, request, jsonify, url_for
import transform
import scrape
import mongodb
import process

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

@app.route("/")
def home():
    return "Hello, Flask!"
  
@app.route("/form", methods=['GET', 'POST']) 
def form():
    if request.method == 'POST':
        # Check if it's a delete request
        if 'deleteTopic' in request.form:
            topic_id = int(request.form.get('topicId'))
            # Call the function to delete the topic and associated data from the database
            mongodb.delete_topic(topic_id)
            return redirect(url_for('form'))

    topics = mongodb.get_all_topics()  # Assume you have a function to get all topics
    return render_template("home.html", topics=topics)

@app.route("/delete_topic", methods=['POST'])
def delete_topic():
    if request.method == 'POST':
        topic_id = int(request.form.get('topicId'))  # Menggunakan request.form untuk mendapatkan data dari form
        if topic_id:
            # Call the function to delete the topic and associated data from the database
            mongodb.delete_topic(topic_id)
            print("TOPIC ID: ", topic_id)
            return jsonify({'message': 'Topic deleted successfully'})
        else:
            return jsonify({'error': 'Invalid request. TopicId is missing.'}), 400
    else:
        return jsonify({'error': 'Invalid request method. Expected POST.'}), 400

@app.route("/hasil") 
def hasil():
    return render_template("hasilAnalisis.html")


@app.route("/get_sentiment_data")
def get_sentiment_data():
    sentiment_data = mongodb.get_sentiment_data()
    return jsonify(sentiment_data)

@app.route("/form_submit", methods=['POST'])
def form_submit():

    # Ambil data di form
    title = request.form.get('title')
    amount_str = request.form.get('amount')
    amount = int(amount_str) if amount_str else 0
    until = request.form.get('endDate')
    since = request.form.get('startDate')

    print(title)
    print(until)
    # Buat topic
    topicId = mongodb.createTopic(title, amount, until, since)

    scrape.crawl_data(topicId, amount, until, since)
    transform.compare_length(topicId)
    transform.trim_field(topicId)
    transform.convert_datetime(topicId)
    transform.add_keyword(topicId)
    process.addLabel(topicId)
    mongodb.insertTweet(topicId)
    mongodb.menghitungSentimen(topicId)

    return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")