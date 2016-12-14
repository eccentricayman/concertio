import urllib2, json
from time import sleep

def key():
    #gets key
    k = open("keys.csv", "r").readline()
    #use index 1 or 3 in next line if you get 403 Forbidden, TEST SPARINGLY ONLY 50 API CALLS / DAY
    k = k.split(",")[3]
    return k

def eventsHelp(z, artist, radius):
    events = []
    u = "http://api.jambase.com/events?api_key=" + key() + "&o=json"
    if z != None:
        z = z.replace(" ", "+")
        u += "&zipCode=" + z + "&radius=" + str(radius) #radius zero so it is only in that zipCode
    if artist != None:
        artist = artist.replace(" ", "+")
        artist = artistId(artist)
        u += "&artistId=" + str(artist)
    urlRequest = urllib2.Request(u, headers={'User-Agent' : "Magic Browser"})
    urlData = urllib2.urlopen(urlRequest)
    data = urlData.read()
    jsonData = json.loads(data)
    eventData = jsonData['Events']
    for event in eventData:
        events += [event['Venue']['Name'], event['Venue']['Address'] + ", " + event['Venue']['City'] + ", " + event['Venue']['State'], event['Id']]
    return events

def artistId(artist):
    artist = artist.replace(" ", "+")
    url = "http://api.jambase.com/artists?name=" + artist + "&api_key=" + key() + "&o=json"
    urlRequest = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
    data = urllib2.urlopen(urlRequest)
    urlData = data.read()
    jsonData = json.loads(urlData)
    artistID = jsonData['Artists'][0]["Id"]
    #need to learn how to use xml
    return artistID

def artistExists(artist):
    artist = artist.replace(" ", "+")
    url = "http://api.jambase.com/artists?name=" + artist + "&api_key=" + key() + "&o=json"
    print url
    urlRequest = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
    data = urllib2.urlopen(urlRequest)
    urlData = data.read()
    jsonData = json.loads(urlData)
    artists = jsonData['Artists']
    return bool(artists);

def events(search):
    return ""

def link(event):
    return ""

def loc(event):
    return ""

def artists(event):
    return ""

def images(event):
    return ""