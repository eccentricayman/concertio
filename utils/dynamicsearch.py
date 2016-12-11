from pyzipcode import ZipCodeDatabase
import jambase
import musixmatch
from pyechonest import config, artist

def search(input):
	try:
		z = int(input)
		if (len(input) == 5):
			#use jambase.py to get the events in this zipcode in a list
			#event list should look like[ [eventname1, eventartist1, eventlocation1], [eventname2, eventartist2, eventlocation2] ]
			events = jambase.eventsHelp(input, None)
	except ValueError:
		zcdb = ZipCodeDatabase()
		#parse yahoo geo.places api GET api here, to see if it's actually a location
		z = zcdb.find_zip(city=input)
		for code in z:
			#use jambase to get all the events, code.zip is the zipcode as a string
			events += jambase.eventsHelp(code.zip, None)
	#now artists
	#same format as eventlist in line 8 of this file, but we're looking for all the events of this artist
	artists = jambase.eventsHelp(None, input)
	#returning the final rendertemplate
	#either eventlist or artistlist can be Nonet
	return render_template("results.html", eventList = events, artistList = artists)

