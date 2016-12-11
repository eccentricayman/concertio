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
    #dynamicsearch is a dictionary of both locations and artist with that name
    return dynamicsearch.search(userInput)
    #event list should look like[ [eventname1, eventartist1, eventlocation1], [eventname2, eventartist2, eventlocation2] ]

@app.route("/results")
def results(resultDict):
    render_template("results.html", results = resultDict)
    ##sends dictionary to html, go thru each entry and format?

##click on some link on results page? searches using jambase for specific event info
@app.route("/event", methods=["POST"])
def event():
    eventID = request.form['event'] ##value of form/link should be event id or event name or something
    eventInfo = results(jambase.events(eventID)) ##waiting on jambase.py for specific formatting 
    render_template("event.html",event = eventInfo)


if __name__ == "__main__":
    app.debug = True
    app.run()
