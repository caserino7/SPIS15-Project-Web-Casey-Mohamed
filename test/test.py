import os
from flask import Flask, url_for, render_template, request
app = Flask(__name__)

##@app.route('/')
##def helloMain():
##    return "Goodbye cruel world!"
##

@app.route('/')
@app.route('/<name>')
def hello(name=None):
    return render_template('Test.html', name=name)

def ftoc(ftemp):
    return (ftemp-32.0)*(5.0/9.0)

def milesToKM(miles):
    return miles * 1.60934

@app.route('/ftoc')
def tempConvert():
    return render_template('ftoc.html')

@app.route('/doTempConvert')
def doTempConvert():
    try:
        ftemp = float(request.args['ftemp'])
        ctemp = ftoc(ftemp)
        return render_template('tempResults.html', showFtemp = ftemp, showCtemp = ctemp)
    except ValueError:
        return render_template('ftoc.html')

@app.route('/mtokm/<milesString>')
def convertMilesToKM(milesString):
    miles = 0.0
    try:
        miles = float(milesString)
        km = milesToKM(miles)
        return milesString + " miles is equal to " + str(km) + " km."
    except ValueError:
        return "Something bad happened. " + milesString + " is invalid."

if __name__=="__main__":
    app.run(port=5001)
    app.run(debug=False)
