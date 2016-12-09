import urllib2
import xml.etree.ElementTree as ET

def key():
    #gets key
    k = open("keys.csv", "r").readline()
    k = k.split(",")[1]
    return k

def eventsHelp(z, artist):
    u = "http://api.jambase.com/events?api_key=" + key()
    if z != null:
        u += "&zipCode=" + z + "&radius=0" #radius zero so it is only in that zipCode
        
    if artist != null:
        artist = artistId(artist)
        u += "&artistId=" + artist

    u = urllib2.urlopen(u)
    u = u.read()
    #need to learn how to use xml
        

def artistId(artist):
    u = "http://api.jambase.com/artists?name=" + artist + "api_key=" + key()
    u = urllib2.urlopen(u)
    u = u.read()
    #need to learn how to use xml
    return "8317"

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


print key()
