import urllib, json
from django.conf import settings
from .config import CREATE_URL
def bioshare_request(url, token, data=None):
    print('bioshare url', url, 'token', token)
    params = json.dumps(data).encode('utf8')
    if data:
        req = urllib.request.Request(url, data=params)
    else:
        req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', 'Token {}'.format(token))
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

def create_share(token, name, description=None):
#         @todo: replace with real API call
#         import string, random
#         return ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(15))
        """
newConditions = {"con1":40, "con2":20, "con3":99, "con4":40, "password":"1234"} 
params = json.dumps(newConditions).encode('utf8')
req = urllib.request.Request(conditionsSetURL, data=params,
                             headers={'content-type': 'application/json'})
response = urllib.request.urlopen(req)
        """
        description = description or 'Genome Center LIMS generated share'
        filesystem = settings.BIOSHARE_SETTINGS.get('DEFAULT_FILESYSTEM',None)
        params = {"name":name,"notes":description,'read_only':False}
        if filesystem:
            params['filesystem'] = filesystem
        return bioshare_post(CREATE_URL, token, params)['id']