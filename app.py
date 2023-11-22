from flask import Flask, render_template, request
import transform
import scrape
import mongodb

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

@app.route("/")
def home():
    return "Hello, Flask!"
  
@app.route("/form") 
def form():
    return render_template("home.html")

@app.route("/form_submit", methods=['POST'])
def form_submit():

    
    # Ambil data di form
    title = request.form.get('title')
    amount_str = request.form.get('amount')
    amount = int(amount_str) if amount_str else 0
    until = request.form.get('endDate')
    since = request.form.get('startDate')

    # Buat tipic
    topicId = mongodb.createTopic(title, amount, until, since)

    scrape.crawl_data(topicId, amount, until, since)
    transform.compare_length(amount)
    transform.trim_field()
    transform.convert_datetime()
    transform.add_keyword()
    return render_template("home.html")



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")