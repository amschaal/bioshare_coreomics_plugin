import urllib, json
def bioshare_request(url, token, data=None):
    params = json.dumps(data).encode('utf8')
    if data:
        req = urllib.request.Request(url, data=params)
    else:
        req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', 'Token %s'%token)
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            data = json.load(response)
            return data
        else:
            raise Exception('API error')
    except urllib.request.HTTPError as e:
        error_message = e.read()
        raise Exception(error_message)
    
def bioshare_post(url, token, data):
    return bioshare_request(url, token, data)

def bioshare_get(url, token):
    return bioshare_request(url, token)