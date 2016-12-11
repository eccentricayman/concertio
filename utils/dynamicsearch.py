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
			#event list should look like[ [eventname1, eventartist1, eventlocation1], [eventname2, eventartist2, eventlocation2] ]
			events = jambase.eventsHelp(input, None)
	except ValueError:
		zcdb = ZipCodeDatabase()
		#parse yahoo geo.places api GET api here, to see if it's actually a location
		parsedInput = input.replace(" ", "+")
		rawData = urllib2.urlopen("http://query.yahooapis.com/v1/public/yql?q=select%20%2a%20from%20geo.places%20where%20text='" + parsedInput + "'&format=json").read()
		data = json.loads(rawData)
		if (data['query']['results'] == None):
			return render_template("home.html", message="Location not found. Please try a zip code or a city.", error=True)
		#yahoo location will get the city where their place is
		placeCity = data['query']['results']['place'][0]['locality1']['content']
		z = zcdb.find_zip(city=placeCity)
		for code in z:
			#use jambase to get all the events, code.zip is the zipcode as a string
			events += jambase.eventsHelp(code.zip, None)
	#now artists
	#same format as eventlist in line 8 of this file, but we're looking for all the events of this artist
	artists = jambase.eventsHelp(None, input)
	#returning the final rendertemplate
	#either eventlist or artistlist can be Nonet
	return render_template("results.html", eventList = events, artistList = artists)

