# Import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Set up application for index.html grabbing data from MongoDB
# @app.route("/")
# def index():
#     #mars = mongo.db.mars.find_one() ### replace with code that pulls specific things 
#     # puts them into an index.html document
#     return render_template("index.html", listings=listings)

# Set up application to create a MongoDB collection
@app.route("/scrape")
def scraper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
