from pyzipcode import ZipCodeDatabase
import jambase, musixmatch
import urllib2, json

def search(input):
	#initializing for the for loop @ line 25
	events = []
	try:
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
				artists = jambase.eventsHelp(None, input)
				return render_template("results.html", eventList = None, artistList = artists)
		#yahoo location will get the city where their place is
		placeCity = data['query']['results']['place'][0]['locality1']['content']
		z = zcdb.find_zip(city=placeCity)
		for code in z:
			#use jambase to get all the events, code.zip is the zipcode as a string
			events += jambase.eventsHelp(code.zip, None)
		#returning the final rendertemplate, either eventList or artistList can be null.
		return render_template("results.html", eventList = events, artistList = None)

