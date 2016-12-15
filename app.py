from flask import Flask, render_template, request, url_for, redirect, session
from utils import jambase, musixmatch, dynamicsearch
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search", methods=["POST"])
def search():
    userInput = request.form["search"]
    if (userInput == ""):
        return render_template("home.html", message="Please search for something!")
    #dynamicsearch is a dictionary of both locations and artist with that name
    searchInfo = dynamicsearch.search(userInput)
    try:
        if (len(searchInfo) == 2):
            return render_template("home.html", message = searchInfo[0], error =searchInfo[1])
        elif (len(searchInfo) == 3):
            return render_template("results.html", eventsList = searchInfo[0], artistList = searchInfo[1], userQuery = searchInfo[2])
    except TypeError:
        return render_template("home.html", message = "We're out of API keys. Sorry for being so cheap.", error = True)

##click on some link on results page? searches using jambase for specific event info
@app.route("/event", methods=["GET", "POST"])
def event():
    eventID = request.args['eventID'] ##value of form/link should be event id or event name or something
    eventInfo = jambase.eventData(eventID) ##waiting on jambase.py for specific formatting
    return render_template("event.html",event = eventInfo)

if __name__ == "__main__":
    app.debug = True
    app.run()
