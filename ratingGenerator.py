import scrape
import random

def rrg():
    for x in scrape.vistaItems:
       print "'"  +  str(x) + "'"  + '=' + str(random.randint(0,1))
    
print rrg()
