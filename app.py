from flask import Flask, render_template, request, url_for, redirect
from ticketmaster import search

@app.route("/")
def search ():
    name= request.form["nameSearch"]
    location= request.form["locationSearch"]
    if (name=="" || location==""):
        return render_template("home.html", message="Please search for something")
    ticketmaster.search(name, location)
            
    


if __name__=="__main__":
    app.debug=True
    app.run()
