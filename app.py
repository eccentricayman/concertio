from flask import Flask, render_template, request, url_for, redirect
from utils import jambase, musixmatch, dynamicsearch, login
import os

app = Flask(__name__)
app.secret_key=os.urandom(32)

@app.route("/")
def home():
    return render_template("home.html", loggedIn?=session['user'])
##user is true if user is logged in

@app.route("/logauthen/")
def log():
    user=request.form["username"]
    password=request.form["password"]
    authen=login.login(user, password)
    if authen=="":
        session['user']=True
    return render_template("home.html", message=authen)

@app.route("/regauthen/")
def reg():
    user=request.form["username"]
    password=request.form["password"]
    authen=login.register(user, password)
    return render_template("home.html", message=authen)

@app.route("/search/", methods=["POST"])
def search():
    userInput = request.form["search"]
    if (userInput == ""):
        return render_template("home.html", message="Please search for something!")
    #dynamicsearch is a dictionary of both locations and artist with that name
    return dynamicsearch.search(userInput)
    #event list should look like[ [eventname1, eventartist1, eventlocation1], [eventname2, eventartist2, eventlocation2] ]

@app.route("/results/")
def results(resultDict):
    render_template("results.html", results = resultDict)
    ##sends dictionary to html, go thru each entry and format?

##click on some link on results page? searches using jambase for specific event info
@app.route("/event/", methods=["POST"])
def event():
    eventID = request.form['event'] ##value of form/link should be event id or event name or something
    eventInfo = results(jambase.events(eventID)) ##waiting on jambase.py for specific formatting 
    render_template("event.html",event = eventInfo)

@app.route("/logout/")
def logout():
    session['user']=False
    redirect(url_for("home"))

if __name__ == "__main__":
    app.debug = True
    app.run()
