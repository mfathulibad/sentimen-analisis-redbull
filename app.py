from flask import Flask, render_template, request, jsonify
import transform
import scrape
import mongodb
import process

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

@app.route("/")
def home():
    return "Hello, Flask!"
  
@app.route("/form") 
def form():
    return render_template("home.html")

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
    # Buat tipic
    # topicId = mongodb.createTopic(title, amount, until, since)

    # scrape.crawl_data(topicId, amount, until, since)
    # transform.compare_length(topicId)
    # transform.trim_field(topicId)
    # transform.convert_datetime(topicId)
    # transform.add_keyword(topicId)
    # process.addLabel(topicId)
    # mongodb.insertTweet(topicId)
    # mongodb.menghitungSentimen(topicId)

    return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")