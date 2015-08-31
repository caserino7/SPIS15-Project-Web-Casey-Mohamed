import os
import psycopg2
import urlparse
#module for building web apps
from flask import Flask, url_for, render_template, request
#module for processing html and xml
from lxml import html
import requests
#imports scrape
import scrape
#imports ratings dictionary
import ratings 


app = Flask(__name__)

#urlparse.uses_netloc.append("postgres")
#url = urlparse.urlparse(os.environ["DATABASE_URL"])

#conn = psycopg2.connect(
#    database=url.path[1:],
#    user=url.username,
#    password=url.password,
#    host=url.hostname,
#    port=url.port
#)

#input = item and item's rating
#outputs thumbs up/down
def rating_for (item, ratings):
    #checks if items is in dictionary
    if item in ratings:
        #if rating returns true: thumbs up
        if ratings[item]:
            return thumbsUp()
        #else thumbs return thumbs down
        else:
            return thumbsDown()
    #return no rating if item isn't in dictionary
    else:
        return ''

#defines image file for thumbs up from glyphicon 
def thumbsUp():
    return ' <span class="glyphicon glyphicon-thumbs-up"></span>' 

#defines image file for thumbs down from glyphicon 
def thumbsDown():
    return ' <span class="glyphicon glyphicon-thumbs-down"></span>'

#helps import ratings dictionary
app.jinja_env.globals.update(rating_for=rating_for)

#home page rendering main.html
@app.route('/')
def renderMain():
    return render_template('main.html')

#defines CV page 
@app.route('/canyonvista')
def renderCV():
    #items variable pulls to scrape.py
    #ratings variable pulls from ratings.py and ratings dictionary
    return render_template('CV.html', breakfast= scrape.allMealItems('Canyon Vista', 'Breakfast'),
                           lunch = scrape.allMealItems('Canyon Vista', 'Lunch'),
                           dinner = scrape.allMealItems('Canyon Vista', 'Dinner'),                           
                           ratings = ratings.ratingsIndex["Canyon Vista"])

#defines 65d's page
@app.route('/64degrees')
def render64d():
    return render_template('64degrees.html')

#defines the pines page
@app.route('/pines')
def renderPines():
    return render_template('pines.html')

if __name__=="__main__":
    app.run(debug=False, host="0.0.0.0", port=10101)
