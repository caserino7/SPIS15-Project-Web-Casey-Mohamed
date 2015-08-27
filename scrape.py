import os
from flask import Flask, url_for, render_template, request
from lxml import html
import requests

app = Flask(__name__)
menuPages = {}
prefix="http://hdh.ucsd.edu/DiningMenus/default.aspx?i="

menuPages['Canyon Vista']=prefix + "24"
menuPages['Cafe Ventanas']=prefix + "18"
menuPages['64 Degrees']=prefix + "64"


page = requests.get(menuPages['Canyon Vista'])
tree = html.fromstring(page.text)

vistaItems = tree.xpath('//form/div[@id="siteContainer"]' +
                       '/div[@id="contentArea"]' +
                       '/div[@id="MenuListing_divRestaurants"]' +
                       '/div' +
                       '/table[@id="MenuListing_tblDaily"]' +
                       '/tr/td/ul[@class="itemList"]' +
                       '/li/a' +
                       '/text()')

print  [vistaItems]

##page = requests.get(menuPages['64 Degrees'])
##tree = html.fromstring(page.text)

##degreeItems = tree.xpath('//form/div[@id="siteContainer"]' +
##                       '/div[@id="contentArea"]' +
##                       '/div[@id="MenuListing_divRestaurants"]' +
##                       '/div' +
##                       '/table[@id="MenuListing_tblDaily"]' +
##                       '/tr/td/ul[@class="itemList"]' +
##                       '/li/a' +
##                       '/text()')
##
##print "degreeItems=" + str(degreeItems)
##
##@app.route('/')
##def main():
##    return render_template('main.html', menu=menuItems)

if __name__=="__main__":
    app.run(port=5000)
    app.run(debug=False)
