# Import dependencies
from flask import Flask, render_template, redirect
import pymongo

# Create an instance of our Flask app
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance
client = pymongo.MongoClient(conn)

# Connect to the mars database. Create it if it doesn't exist.
db = client.mars_db

# Drops collection 'mars' if available to remove any duplicates when we populate
# the very same collection of 'mars' below.
db.mars.drop()

# Set up application for index.html grabbing data from MongoDB.
@app.route("/")
def index():
    mars = db.mars#list(db.mars.find())
    return render_template("index.html", mars=mars)

# Set up application to create a MongoDB collection
@app.route("/scrape")
def scraper():
    import scrape_mars

    mars_collection = db.mars
    mars_data = scrape_mars.scrape()
    mars_collection.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)