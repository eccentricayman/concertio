from pyzipcode import ZipCodeDatabase

def search(input):
	try:
		z = int(input)
		if (len(z.zip) == 5):
			#use jambase.py to get the events in this zipcode in a list
			#event list should look like[ [eventname1, eventartist1, eventlocation1], [eventname2, eventartist2, eventlocation2] ]
			events = eventsHelp(z.zip, null)
	except ValueError:
		zcdb = ZipCodeDatabase()
		z = zcdb.find_zip(city=input)
		for code in z:
			#use jambase to get all the events, code.zip is the zipcode as a string
			events += eventsHelp(code.zip, null)
	#now artists
	#same format as eventlist in line 8 of this file, but we're looking for all the events of this artist
	artists = eventsHelp(null, input)
	#returning the final rendertemplate
	return render_template("results.html", eventList = events, artistList = artists)
