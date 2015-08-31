import os
from flask import Flask, url_for, render_template, request
from lxml import html
import requests
import scrape
import ratings 



app = Flask(__name__)

def rating_for (item, ratings):
    if item in ratings:
        if ratings[item]:
            return thumbsUp()
        else:
            return thumbsDown()
    else:
        return ''

def thumbsUp():
    return '<span class="glyphicon glyphicon-thumbs-up"></span>' 

def thumbsDown():
    return '<span class="glyphicon glyphicon-thumbs-down"></span>'

app.jinja_env.globals.update(rating_for=rating_for)

@app.route('/')
def renderMain():
    return render_template('main.html')
#add ~ 9 more pages for 3 meals at every hall

@app.route('/canyonvista')
def renderCV():
    return render_template('CV.html', items= scrape.vistaItems,
                           ratings = ratings.ratingsIndex["Canyon Vista"])

@app.route('/64degrees')
def render64d():
    return render_template('64degrees.html')

@app.route('/pines')
def renderPines():
    return render_template('pines.html')


if __name__=="__main__":
    app.run(debug=False, host="0.0.0.0", port=10101)
