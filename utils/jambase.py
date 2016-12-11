import urllib2, json

def key():
    #gets key
    k = open("keys.csv", "r").readline()
    k = k.split(",")[1]
    return k

def eventsHelp(z, artist):
    u = "http://api.jambase.com/events?api_key=" + key() + "&o=json"
    if z != None:
        u += "&zipCode=" + z + "&radius=0" #radius zero so it is only in that zipCode
        
    if artist != None:
        artist = artistId(artist)
        u += "&artistId=" + str(artist)

    print u
    u = urllib2.urlopen(u)
    urlData = u.read()
    jsonData = json.loads(urlData)
    #examplu (first from http://pastebin.com/bWRSCvqm)
    return [ ["The Great Northern", 2873583, "119 Utah Street, San Francisco, California"], ["Halcyon", 160644, "314 11th Street, San Francisco, California"] ]
    
def artistId(artist):
    artist = artist.replace(" ", "+")
    url = "http://api.jambase.com/artists?name=" + artist + "&api_key=" + key() + "&o=json"
    data = urllib2.urlopen(url)
    urlData = data.read()
    jsonData = json.loads(urlData)
    artistID = jsonData['Artists'][0]["Id"]
    #need to learn how to use xml
    return artistID

def artistExists(artist):
    artist = artist.replace(" ", "+")
    url = "http://api.jambase.com/artists?name=" + artist + "&api_key=" + key() + "&o=json"
    data = urllib2.urlopen(url)
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
