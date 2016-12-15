from flask import Flask, render_template, request, url_for, redirect, session
from utils import jambase, musixmatch, dynamicsearch, login
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/")
def home():
    try:
        return render_template("home.html", loggedIn = session['user'])
    except KeyError:
        return render_template("home.html", loggedIn = False)
##logged in is a boolean user is true if user is logged in
## used in html to check if register/login buttons should show up

@app.route("/authenticate")
def log():
    user=request.form["username"]
    password=request.form["password"]
    whichButton = request.form["submitButton"]
    if (whichButton == "Login"):
        authen=login.login(user, password)
        if authen=="":
            session['user']=True
            hasError = False
        else:
            hasError = True
    if (whichButton == "Register"):
        authen = login.register(user, password)
        if authen == "":
            hasError = False
        else:
            hasError = True
    return render_template("home.html", message=authen, error = hasError)

@app.route("/search", methods=["POST"])
def search():
    userInput = request.form["search"]
    if (userInput == ""):
        return render_template("home.html", message="Please search for something!")
    #dynamicsearch is a dictionary of both locations and artist with that name
    searchInfo = dynamicsearch.search(userInput)
    if (len(searchInfo) == 2):
        return render_template("home.html", message = searchInfo[0], error =searchInfo[1])
    elif (len(searchInfo) == 3):
        return render_template("results.html", eventsList = searchInfo[0], artistList = searchInfo[1], userQuery = searchInfo[2])
    else:
        return render_template("home.html", message = "Unknown error. Please try again.", error = True)

##click on some link on results page? searches using jambase for specific event info
@app.route("/event", methods=["GET", "POST"])
def event():
    eventID = request.args['eventID'] ##value of form/link should be event id or event name or something
    eventInfo = jambase.eventData(eventID) ##waiting on jambase.py for specific formatting
    return render_template("event.html",event = eventInfo)

@app.route("/logout")
def logout():
    session['user']=False
    redirect(url_for("home"))

if __name__ == "__main__":
    app.debug = True
    app.run()
