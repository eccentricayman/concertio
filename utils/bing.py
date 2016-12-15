import httplib, urllib, base64, json

def key():
	k = open("keys.csv", "r").readline();
	k = k.split(",")[5]
	return k

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': key(),
}

def getImage(query):
	params = urllib.urlencode({
	    # Request parameters
	    'q': query,
	    'count': '50',
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
	    images = parsedData['value']
	    for image in images:
	    	if (image['height'] == image['width']):
	    		return image['contentUrl']
	    ratio = 0
	    for image in images:
	    	if (abs(1 - image['height'] / image['width']) < abs(1 - ratio)):
	    		ratio = image['height'] / image['width']
	    for image in image:
	    	if ((image['height'] / image['width']) == ratio):
				return image['contentUrl']
	except Exception as e:
		return "static/placeholder.png"

def getNonSquareImage(query):
	params = urllib.urlencode({
	    # Request parameters
	    'q': query,
	    'count': '50',
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
	    images = parsedData['value']
	    return images[0]['contentUrl']
	except Exception as e:
		return "static/placeholder.png"