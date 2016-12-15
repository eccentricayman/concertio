import urllib2, json
import bing, musixmatch

def key():
    #gets key
    k = open("keys.csv", "r").readline()
    #use index 1 or 3 in next line if you get 403 Forbidden, TEST SPARINGLY ONLY 50 API CALLS / DAY
    k = k.split(",")[6]
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
    print u
    urlRequest = urllib2.Request(u, headers={'User-Agent' : "Magic Browser"})
    urlData = urllib2.urlopen(urlRequest)
    data = urlData.read()
    jsonData = json.loads(data)
    eventData = jsonData['Events']
    for event in eventData:
        if (not eventExists(events, event['Venue']['Name'])):
            events.append([event['Venue']['Name'], event['Venue']['Address'] + ", " + event['Venue']['City'] + ", " + event['Venue']['State'], event['Id'], bing.getImage(event['Venue']['Name'])])
    return events

def eventExists(eventList, name):
    for event in eventList:
        if (event[0] == name):
            return True
    return False

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
    urlRequest = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
    data = urllib2.urlopen(urlRequest)
    urlData = data.read()
    jsonData = json.loads(urlData)
    artists = jsonData['Artists']
    return bool(artists);

def eventData(event):
    url = "http://api.jambase.com/events?id=" + str(event) + "&api_key=" + key() + "&o=json"
    urlRequest = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
    data = urllib2.urlopen(urlRequest)
    urlData = data.read()
    eventData = json.loads(urlData)
    print eventData
    eventDataList = [eventData['Venue']['Name'], eventData['Venue']['Address'] + ", " + eventData['Venue']['City'] + ", " + eventData['Venue']['State'], eventData['Date'], bing.getNonSquareImage(eventData['Venue']['Name']), eventData['TicketUrl']]
    artistDataList = []
    for artist in eventData['Artists']:
        artistDataList.append([artist['Name'], bing.getImage(artist['Name']), musixmatch.toptracks(artist['Name'])])
    eventDataList.append(artistDataList)
    print "\n\n\n"
    print eventDataList[5]
    print "\n\n\n"
    return eventDataList

