import os
#module for building web apps
from flask import Flask, url_for, render_template, request
#module for processing html and xml
from lxml import html
import requests

#empty variable for dining menus
menuPages = {}
#base url for the dining hall menus
prefix="http://hdh.ucsd.edu/DiningMenus/default.aspx?i="

#defines the three dining halls w/ their i= value
menuPages['Canyon Vista']=prefix + "24"
menuPages['Cafe Ventanas']=prefix + "18"
menuPages['64 Degrees']=prefix + "64"

#requests CV's menu page
page = requests.get(menuPages['Canyon Vista'])
#utilizes requests/tree to scrape
tree = html.fromstring(page.text)

menuItemsXPath = ('//form/div[@id="siteContainer"]' +
                       '/div[@id="contentArea"]' +
                       '/div[@id="MenuListing_divRestaurants"]' +
                       '/div' +
                       '/table[@id="MenuListing_tblDaily"]' +
                       '/tr/td/ul[@class="itemList"]' +
                       '/li/a' +
                       '/text()')

def mealXPath(mealNum):
   '''1 for breakfast, 2 for lunch, 3 for dinner'''
   return ('//form/div[@id="siteContainer"]' +
                       '/div[@id="contentArea"]' +
                       '/div[@id="MenuListing_divRestaurants"]' +
                       '/div' +
                       '/table[@id="MenuListing_tblDaily"]' +
                       '/tr[3]/td[' + str(mealNum) + ']/ul[@class="itemList"]' +
                       '/li/a' +
                       '/text()')

#directs to where in the source page to scrape menu data
def allMenuItems(diningHall):
   page = requests.get(menuPages[diningHall])
   tree = html.fromstring(page.text)
   return tree.xpath(menuItemsXPath)

mealNums = {"Breakfast": 1, "Lunch": 2, "Dinner": 3}

def allMealItems(diningHall, meal):
   page = requests.get(menuPages[diningHall])
   tree = html.fromstring(page.text)
   return tree.xpath(mealXPath(mealNums[meal]))

vistaItems = allMenuItems('Canyon Vista')
vistaBreakfast = allMealItems('Canyon Vista', 'Breakfast')
vistaLunch = allMealItems('Canyon Vista', 'Lunch')
vistaDinner = allMealItems('Canyon Vista', 'Dinner')

#vistaBreakfast = []
#for i in range(len(vistaItems)):
#   vistaBreakfast.insert(i, vistaItems[i])
#   if vistaItems[i] == 'Yogurt Bar':
#      break

#64d's implementation
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


if __name__=="__main__":
#   print str(vistaItems)
   print str(vistaBreakfast)
   print str(vistaLunch)
   print str(vistaDinner)
#   print str(vistaBreakfast)
