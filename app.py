from flask import Flask, render_template, request
import transform
import scrape

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
    # Get the values of "topicTitle" and "totalData" from the form
    # topic_title = request.form.get('topicTitle', '')
    total_data = int(request.form.get('totalData', 50))  # Default to 50 if not provided

    # Call crawl_data with dynamic parameters
    scrape.crawl_data(limit=total_data)
    # scrape.crawl_data()
    transform.compare_length(50)
    transform.trim_field()
    transform.convert_datetime()
    transform.add_keyword()
    return render_template("home.html")



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")