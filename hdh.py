import os
from flask import Flask, url_for, render_template, request
from lxml import html
import requests

app = Flask(__name__)

@app.route('/')
def renderMain():
    return render_template('main.html')

if __name__=="__main__":
    app.run(debug=False, host="0.0.0.0", port=55555)
