from pyzipcode import ZipCodeDatabase
import jambase, musixmatch
from flask import *
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
				events = jambase.eventsHelp(input, None, 0)
				return [events, None, input]
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
					return ["Error: Not found. Please search an artist OR a location, not both.", True]
				else:
					artists = jambase.eventsHelp(None, input, 0)
					return [None, artists, input]
			elif (isinstance(data['query']['results']['place'], list)):
				if (data['query']['results']['place'][0]['country']['content'] != "United States"):
					if (jambase.artistExists(input) == False):
						return ["All locations must be within the United States.", False]
					else:
						artists = jambase.eventsHelp(None, input, 0)
						return [None, artists, input]
			elif (not isinstance(data['query']['results']['place'], list)):
				if (data['query']['results']['place']['country']['content'] != "United States"):
					if (jambase.artistExists(input) == False):
						return ["All locations must be within the United States.", False]
					else:
						artists = jambase.eventsHelp(None, input, 0)
						return [None, artists, input]
			else:
				#yahoo location will get the city where their place is
				placeCity = data['query']['results']['place'][0]['locality1']['content']
				z = zcdb.find_zip(city=placeCity)
				#50 radius
				events = jambase.eventsHelp(z[len(z) / 2].zip, None, 50)
				#returning the final rendertemplate, either eventList or artistList can be null.
				return [events, None, input]
	except urllib2.HTTPError:
		return ["Too many API requests, please try again in a day.", True]
	#return render_template("results.html", userQuery = "New York", eventsList = [['Madison Square Garden', '7th Avenue & 32nd Street, New York, New York', 2747828, None], ['BB&T Center', 'One Panther Parkway, Fort Lauderdale, Florida', 2858011, 'https://www.bing.com/cr?IG=DA3740A3A06046B4A589DB3C3709CA91&CID=2B6B3CAED95666F718573545D8676755&rd=1&h=zJtZFEODmTVQLjjtDFmc_ALRfWlyrzQjyBVwCz9_Puk&v=1&r=https%3a%2f%2fpbs.twimg.com%2fprofile_images%2f2596282241%2fz770oyecq0vacwu6n4zn_400x400.jpeg&p=DevEx,5170.1'], ['Madison Square Garden', '7th Avenue & 32nd Street, New York, New York', 2874737, None, 'Amway Center', '400 West Church Street, Orlando, Florida', 2861803, 'http://www.bing.com/cr?IG=F9104B976035456B87BB3501BE93349B&CID=0047D0043BEB65B60C7FD9EF3ADA6471&rd=1&h=ohR5E9o_z2fyW0HG6g_q-8zUoAyMrUnv_Fu3-_B8l7I&v=1&r=http%3a%2f%2fwww.gotickets.com%2fcached%2f_images%2fmaintainwidth%2f521x750%2f3289d6466a2cd8483042263f956c9f7d%2famway-arena-1757.gif&p=DevEx,5236.1'], ['Smoothie King Center', '1501 Girod Street, New Orleans, Louisiana', 2874738, None], ['Madison Square Garden', '7th Avenue & 32nd Street, New York, New York', 2881111, None], ['Madison Square Garden', '7th Avenue & 32nd Street, New York, New York', 2890258, None], ['Pinnacle Bank Arena ', '600 R Street, Lincoln, Nebraska', 2874739, "https://www.bing.com/cr?IG=4674CD7A99BF44BE9C021EABFDDA3AAE&CID=0BD5603ADFBC6D822F3369D1DE8D6CB7&rd=1&h=1USc8weX_DJQ8_7DYAJOyN7ZEEMCajS5GhkWejHf78Y&v=1&r=https%3a%2f%2firs0.4sqi.net%2fimg%2fgeneral%2f600x600%2f58925183_ofKa2vrGqPapaZ0PBkyQI9bzeaBY-5tl73hdUsrRWns.jpg&p=DevEx,5152.1"], ["Nassau Coliseum", '1255 Hempstead Tpke, Uniondale, New York', 2860811, None]], artistList = None)

