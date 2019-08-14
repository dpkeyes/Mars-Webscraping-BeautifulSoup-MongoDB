# Import dependencies
from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Create an instance of our Flask app
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance
client = pymongo.MongoClient(conn)

# Connect to the mars database. Create mars_db if it doesn't exist.
db = client.mars_db

# Set up application for index.html grabbing data from MongoDB.
@app.route("/")
def index():
    try:
        mars = db.mars.find_one()
    except:
        pass
    print(mars)
    return render_template("index.html", mars=mars)

# Set up application to create a MongoDB collection
@app.route("/scrape")
def scraper():
    mars_data = scrape_mars.scrape()
    db.mars.update_one({}, mars_data, upsert=True)
    return redirect("/")

# Normal conclusion to Flask application
if __name__ == "__main__":
    app.run(debug=True)