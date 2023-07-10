from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import main
from pymongo.mongo_client import MongoClient

app = Flask(__name__)
uri = "mongodb+srv://TheSilentCoders:thesilentcoders@cluster0.x1ymrhc.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@app.route("/", methods = ['GET', 'POST'])
def home():
    return render_template("search.html")

@app.route("/review", methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ", "")
            amazonReviewResult = main.wholeReviewProcess(searchString = searchString)
            db = client['Amazon_Review_Scrapper']
            review_coll = db['Amazon_Review_Scrapper_data']
            review_coll.insert_many(amazonReviewResult)
            return render_template("review-page.html", reviews = amazonReviewResult[0:len(amazonReviewResult)-1])
        except Exception as e:
            main.logging.info(e)
            return render_template("serverError.html")
    else:
        return render_template("search.html")
    
app.run(debug = True)