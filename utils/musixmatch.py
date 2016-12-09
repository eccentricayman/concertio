import urllib2
import json

def toptracks (artist):#takes artist name as string
    u = "http://api.musixmatch.com/ws/1.1/track.search?q_artist=" + artist + "&s_track_rating=desc&apikey=" + key()
    u = urllib2.urlopen(u)
    u = u.read()
    u = json.loads(u)
    u = u["message"]["body"]["track_list"]
    for i in range(10):
        u[i] = u[i]["track"]
    return u
#returns a list of ten dictionaries, each dictionary is a track
#important keys are:
####"track_name"
####"album_name"
####"album_coverart_100x100"
####"track_share_url" - note that this is a link to the musixmatch page of lyrics


##HELPERS##
def key():
    #gets key
    
    k = open("keys.csv", "r").readline()
    k = k.split(",")[0]
    return k

print toptracks("radiohead")
