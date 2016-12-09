from flask import Flask, render_template, request, url_for, redirect
from utils import jambase, musixmatch, dynamicsearch

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search", methods=["POST"])
def search():
    userInput = request.form["search"]
    if (userInput == ""):
        return render_template("home.html", message="Please search for something!")
    #dynamicsearch will run results from the search function; i'll call jambase and musixmatch
    #from there, and it'll return 0 if it can't tell what place it is
    whichSearch = dynamicsearch.search(userInput)
    if (whichSearch == False):
    	return render_template("home.html", message="Please be more specific.", error = True)
    ## events from jambase should return a dictionary in format of {event0ID:[link, artist, etc], event1ID:[same]}

@app.route("/results")
def results(resultDict):
    render_template("results.html", results = resultDict)
    ##sends dictionary to html, go thru each entry and format?

##click on some link on results page? searches using jambase for specific event info    
@app.route("/event", methods=["GET"])
def event():
    eventID = request.form['event']
    eventInfo = results(jambase.events(eventID))
    render_template("event.html",event = eventInfo)
    

if __name__ == "__main__":
    app.debug = True
    app.run()
