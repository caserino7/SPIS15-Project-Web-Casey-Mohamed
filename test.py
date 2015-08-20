from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Goodbye cruel world!"

def ftoc(ftemp):
    return (ftemp-32.0)*(5.0/9.0)

def milesToKM(miles):
    return miles * 1.60934

@app.route('/ftoc/<ftempString>')
def convertFtoC(ftempString):
    ftemp = 0.0
    try:
        ftemp = float(ftempString)
        ctemp = ftoc(ftemp)
        return "In Farenheit: " + ftempString + " In Celsius: " + str(ctemp)
    except ValueError:
        return "Sorry. Couldn't convert " + ftempString + " to a number."

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
    app.run(port=5000)
    app.run(debug=False)
