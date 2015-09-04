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

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

cursor = conn.cursor()

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

#gets the ratings from the database
def getRatingsFromHall(diningHall):
    ratings = {}
    cursor.execute("SELECT item,rating FROM ratings WHERE dining_hall='" + diningHall + "';")
    while True:
        data = cursor.fetchone()
        if data == None:
            break
        ratings[str(data[0])] = data[1]
    return ratings

def renderPage(diningHall):
	if diningHall == 'Canyon Vista':
		return renderCV()
	elif diningHall == '64 Degrees':
		return render64d()
	elif diningHall == "Pines":
		return renderPines()
	else:
		return renderMain()

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

#modifies the database based on user input
@app.route('/addRating/<diningHall>/<item>', methods=('GET', 'POST'))
def addRating(diningHall, item):
	rating = request.form['rating']
	command = "SELECT rating FROM ratings WHERE dining_hall='" + diningHall + "' and item='" + item + "';"
	before = ['']
	cursor.execute(command)
	data = cursor.fetchone()
	if data != None:
		before[0] = data[0]
	if before[0] == '':
		if rating != '':
			command = "INSERT INTO ratings VALUES ('" + diningHall + "', '" + item + "', " + rating + ");"
			cursor.execute(command)
			conn.commit()
			return renderPage(diningHall)
		else:
			return renderPage(diningHall)
	elif rating == '':
		command = "DELETE FROM ratings WHERE dining_hall='" + diningHall + "' and item='" + item + "';"
		cursor.execute(command)
		conn.commit()
		return renderPage(diningHall)
	elif  before[0] != rating:
		command = "UPDATE ratings SET rating='" + rating + "' WHERE dining_hall='" + diningHall + "' and item='" + item + "';"
		cursor.execute(command)
		conn.commit()
		return renderPage(diningHall)
	else:
		return renderPage(diningHall)
		
#defines CV page 
@app.route('/canyonvista')
def renderCV():
    #items variable pulls to scrape.py
    #ratings variable pulls from ratings.py and ratings dictionary
    print "This is renderCV()"
    return render_template('CV.html', breakfast = scrape.allMealItems('Canyon Vista', 'Breakfast'),
                           lunch = scrape.allMealItems('Canyon Vista', 'Lunch'),
                           dinner = scrape.allMealItems('Canyon Vista', 'Dinner'),
                           ratings = getRatingsFromHall('Canyon Vista'),
                           diningHall = 'Canyon Vista')

#defines 64d's page
@app.route('/64degrees')
def render64d():
    return render_template('64degrees.html', breakfast = scrape.allMealItems('64 Degrees', 'Breakfast'),
                           lunch = scrape.allMealItems('64 Degrees', 'Lunch'),
                           dinner = scrape.allMealItems('64 Degrees', 'Dinner'),
                           ratings = getRatingsFromHall('64 Degrees'),
                           diningHall = '64 Degrees')

#defines the pines page
@app.route('/pines')
def renderPines():
    return render_template('pines.html', breakfast = scrape.allMealItems('Pines', 'Breakfast'),
                           lunch = scrape.allMealItems('Pines', 'Lunch'),
                           dinner = scrape.allMealItems('Pines', 'Dinner'),
                           ratings = getRatingsFromHall('Pines'),
                           diningHall = 'Pines')

if __name__=="__main__":
    app.run(debug=False, host="0.0.0.0", port=10101)
