import re
import urllib, json
from django.conf import settings
from rest_framework import exceptions, status as drf_status
from .config import CREATE_URL, GET_URL


class BioshareAPIError(exceptions.APIException):
    """Bioshare API returned an error; surface its detail to our API client.

    Raised by bioshare_request when the upstream Bioshare server responds with
    a non-2xx status or is unreachable. Subclassing APIException means DRF's
    exception handler renders the structured `detail` back to the client
    (e.g. {"link_to_path": ["Path not allowed."]}) instead of returning 500.
    """
    status_code = drf_status.HTTP_502_BAD_GATEWAY
    default_detail = 'Bioshare API error.'
    default_code = 'bioshare_error'

    def __init__(self, detail=None, status_code=None):
        if status_code is not None:
            self.status_code = status_code
        super().__init__(detail=detail)


def _parse_bioshare_error(body, upstream_status):
    """Turn a Bioshare error response body into (detail, http_status)."""
    if isinstance(body, bytes):
        body = body.decode('utf-8', errors='replace')
    try:
        payload = json.loads(body) if body else None
    except ValueError:
        payload = None
    if isinstance(payload, dict):
        # Bioshare wraps field errors as {"errors": {...}}; unwrap so the
        # response matches DRF's standard per-field validation shape.
        detail = payload.get('errors', payload)
    elif payload is not None:
        detail = payload
    else:
        detail = body or 'Bioshare API error.'
    # 4xx -> pass-through; 5xx / unknown -> 502 Bad Gateway.
    status_code = (upstream_status if 400 <= upstream_status < 500
                   else drf_status.HTTP_502_BAD_GATEWAY)
    return detail, status_code


def bioshare_request(url, token, data=None):
    print('bioshare url', url, 'token', token)
    if data:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf8'))
    else:
        req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', 'Token {}'.format(token))
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        detail, status_code = _parse_bioshare_error(e.read(), e.code)
        raise BioshareAPIError(detail=detail, status_code=status_code) from e
    except urllib.error.URLError as e:
        raise BioshareAPIError(
            detail='Could not reach Bioshare: {}'.format(e.reason),
            status_code=drf_status.HTTP_502_BAD_GATEWAY,
        ) from e
    if response.getcode() == 200:
        return json.load(response)
    raise BioshareAPIError(
        detail='Unexpected HTTP {} from Bioshare.'.format(response.getcode()),
        status_code=drf_status.HTTP_502_BAD_GATEWAY,
    )

def parse_share_id(url):
    SHARE_REGEX = r'^https?:\/\/.+\/bioshare\/view\/(?P<share>[a-zA-Z0-9]{15})\/?$'
    matches = re.match(SHARE_REGEX, url)
    if not matches:
        return None
    return matches[1]

def bioshare_post(url, token, data):
    return bioshare_request(url, token, data)

def bioshare_get(url, token):
    return bioshare_request(url, token)

def get_share(token, id):
    url = GET_URL.format(id=id)
    return bioshare_get(url, token)

def create_share(token, name, description=None, filesystem=None, link_to_path=None):
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
        # filesystem = settings.BIOSHARE_SETTINGS.get('DEFAULT_FILESYSTEM',None)
        params = {"name":name,"notes":description,'read_only':False}
        if filesystem:
            params['filesystem'] = filesystem
        if link_to_path:
            params['link_to_path'] = link_to_path
            params['read_only'] = True
        return bioshare_post(CREATE_URL, token, params)['id']