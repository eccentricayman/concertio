#626c4n8t8x4dy4qxs5jfuy4k
import urllib2
import xml.etree.ElementTree as ET

#def events(search):
    

def eventsHelp(z, artist):
    u = "http://api.jambase.com/events?api_key=626c4n8t8x4dy4qxs5jfuy4k"
    if z != null:
        u += "&zipCode=" + z + "&radius=0" #radius zero so it is only in that zipCode
        
    if artist != null:
        artist = artistId(artist)
        u += "&artistId=" + artist

    u = urllib2.urlopen(u)
    u = u.read()
    #need to learn how to use xml


        

def artistId(artist):
    u = "http://api.jambase.com/artists?api_key=626c4n8t8x4dy4qxs5jfuy4k&name=" + artist
    u = urllib2.urlopen(u)
    u = u.read()
    #need to learn how to use xml
    return "8317"

#def link(event):

#def loc(event):

#def artists(event):
    
#def images(event):

