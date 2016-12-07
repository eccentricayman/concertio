from flask import Flask, render_template, request, url_for, redirect
from jambase import events

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search", methods=["POST"])
def search ():
    userinput= request.form["search"]
    if (userinput==""):
        return render_template("home.html", message="Please search for something")
    results(jambase.events(userinput))

@app.route("/results")
def results():
    render_template("results.html")

@app.route("/event", methods=["GET"])
def event():
    render_template("event.html")
    


if __name__=="__main__":
    app.debug=True
    app.run()
