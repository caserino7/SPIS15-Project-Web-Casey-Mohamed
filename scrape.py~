from lxml import html
import requests

menuPages = {}
prefix="http://hdh.ucsd.edu/DiningMenus/default.aspx?i="

menuPages['Canyon Vista']=prefix + "24"
menuPages['Cafe Ventanas']=prefix + "18"
menuPages['64 Degrees']=prefix + "64"


page = requests.get(menuPages['Canyon Vista'])
tree = html.fromstring(page.text)

menuItems = tree.xpath('//form/div[@id="siteContainer"]' +
                       '/div[@id="contentArea"]' +
                       '/div[@id="MenuListing_divRestaurants"]' +
                       '/div' +
                       '/table[@id="MenuListing_tblDaily"]' +
                       '/tr/td/ul[@class="itemList"]' +
                       '/li/a' +
                       '/text()')

print "menuItems=" + str(menuItems)
