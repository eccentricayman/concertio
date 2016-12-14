from pyzipcode import ZipCodeDatabase
import jambase, musixmatch
from flask import render_template
import urllib2, json

def search(input):
	#initializing for the for loop @ line 25
	try:
		events = []
		try:
			#testing if it's an int and if it's length is 5 (zip code reqs)
			z = int(input)
			if (len(input) == 5):
				#use jambase.py to get the events in this zipcode in a list
				#event list should look like[ [eventname1, eventid1, eventlocation1], ...]
				events = jambase.eventsHelp(input, None)
		except ValueError:
			zcdb = ZipCodeDatabase()
			#parse yahoo geo.places api GET api here, to see if it's actually a location
			parsedInput = input.replace(" ", "+")
			rawData = urllib2.urlopen("http://query.yahooapis.com/v1/public/yql?q=select%20%2a%20from%20geo.places%20where%20text='" + parsedInput + "'&format=json").read()
			data = json.loads(rawData)
			#check if any places with this name exist
			if (data['query']['results'] == None):
				#check if artist exists
				if (jambase.artistExists(input) == False):
					return render_template("home.html", message="Error: Not found. Please search an artist OR a location, not both.", error = True)
				else:
					artists = jambase.eventsHelp(None, input, 0)
					return render_template("results.html", eventList = None, artistList = artists)
			elif (data['query']['results']['place'][0]['country']['content'] != "United States"):
				if (jambase.artistExists(input) == False):
					return render_template("home.html", message="All locations must be within the United States.", error = False)
				else:
					artists = jambase.eventsHelp(None, input, 0)
					return render_template("results.html", eventList = None, artistList = artists)
			else:
				#yahoo location will get the city where their place is
				placeCity = data['query']['results']['place'][0]['locality1']['content']
				z = zcdb.find_zip(city=placeCity)
				#50 radius
				events = jambase.eventsHelp(z[len(z) / 2].zip, None, 50)
				#returning the final rendertemplate, either eventList or artistList can be null.
				return render_template("results.html", eventList = events, artistList = None)
	except urllib2.HTTPError:
		return render_template("home.html", message = "Too many API requests, please try again in a day.", error = True)
