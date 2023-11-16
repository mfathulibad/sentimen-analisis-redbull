from flask import Flask, render_template
import transform
import scrape

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"
  
@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/form_submit", methods=['POST'])
def form_submit():
    #scrape.crawl_data()
    transform.compare_length(50)
    transform.trim_field()
    transform.convert_datetime()
    transform.add_keyword()
    return render_template("form.html")



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")