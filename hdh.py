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
    print cursor
    ratings = {}
    cursor.execute("SELECT item,rating FROM ratings WHERE dining_hall='" + diningHall + "';")
    while True:
        data = cursor.fetchone()
        if data == None:
            break
        ratings[str(data[0])] = data[1]
    return ratings

#adds a rating to the database
def addRating(diningHall, item, rating):
    cursor.execute("INSERT INTO ratings VALUES ('" + diningHall + "', '" + item + "', " + rating + ");")

#changes the rating of a specific item at a specific dining hall
def changeRating(diningHall, item, newRating):
    cursor.execute("UPDATE ratings SET rating='" + newRating + "' WHERE diningHall='" + diningHall + "' and item='" + item + "';")

#deletes a rating from the database
def deleteRating(diningHall, item):
    cursor.execute("DELETE FROM ratings WHERE diningHall='" + diningHall + "' and item='" + item + "';")

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

@app.route('/addRating/<diningHall>/<item>', methods=('GET', 'POST'))
def addRating(diningHall, item):
	rating = request.form['rating']
	print rating
	command = "SELECT rating FROM ratings WHERE dining_hall='" + diningHall + "' and item='" + item + "';"
	print command
	before = []
	print 'blah'
	cursor.execute(command)
	print 'blah'
	data = cursor.fetchone()
	print 'blah3'
	if data != None:
		print 'blah'
		before[0] = data[0]
	print "data: " + before
	if before == []:
		if rating != '':
			command = "INSERT INTO ratings VALUES ('" + diningHall + "', '" + item + "', " + rating + ");"
			cursor.execute(command)
			conn.commit()
			return renderCV()
		else:
			return renderCV()
	elif rating == '':
		command = "DELETE FROM ratings WHERE dining_hall='" + diningHall + "' and item='" + item + "';"
		cursor.execute(command)
		conn.commit()
		return renderCV()
	elif  before[0] != rating:
		command = "UPDATE ratings SET rating='" + rating + "' WHERE dining_hall='" + diningHall + "' and item='" + item + "';"
		cursor.execute(command)
		conn.commit()
		return renderCV()
	else:
		return renderCV()
		
# def addRating(diningHall, item):
    # print "request.method = " + request.method
    # print "dining hall: " + diningHall + " item: " + item
    # rating = request.form['rating']
    # print "dining hall: " + diningHall + " item: " + item + " rating: " + rating
    # command = "INSERT INTO ratings VALUES ('" + diningHall + "', '" + item + "', " + rating + ");"
    # print cursor
    # print command
    # cursor.execute(command)
    # print "Commiting"
    # conn.commit()
    # print "dcj"
    # print "url_for = " + url_for('renderCV')
    # return renderCV()

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

#defines 65d's page
@app.route('/64degrees')
def render64d():
    return redirect('https://www.google.com')

#defines the pines page
@app.route('/pines')
def renderPines():
    return render_template('pines.html')

if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0", port=10101)
