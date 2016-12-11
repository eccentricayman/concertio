import httplib, urllib, base64, json

def key():
	k = open("keys.csv", "r").readline();
	k = k.split(",")[2]
	return k

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': key(),
}

def getImage(query):
	params = urllib.urlencode({
	    # Request parameters
	    'q': query,
	    'count': '1',
	    'offset': '0',
	    'mkt': 'en-us',
	    'safeSearch': 'Moderate',
	})

	try:
	    conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
	    conn.request("GET", "/bing/v5.0/images/search?%s" % params, "{body}", headers)
	    response = conn.getresponse()
	    data = response.read()
	    conn.close()
	    parsedData = json.loads(data)
	    return (parsedData['value'][0]['contentUrl'])
	except Exception as e:
	    return None
