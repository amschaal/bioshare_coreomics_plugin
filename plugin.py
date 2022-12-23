from django.conf import settings
CREATE_URL = settings.BIOSHARE_SETTINGS['URL'] + '/bioshare/api/shares/create/'
VIEW_URL = settings.BIOSHARE_SETTINGS['URL'] + '/bioshare/view/{id}/'
GET_PERMISSIONS_URL = settings.BIOSHARE_SETTINGS['URL'] + '/bioshare/api/get_permissions/{id}'
SET_PERMISSIONS_URL = settings.BIOSHARE_SETTINGS['URL'] + '/bioshare/api/set_permissions/{id}'

from plugins import Plugin
from .urls import urlpatterns
from .forms import form
class PPMSPlugin(Plugin):
    ID = 'bioshare'
    SUBMISSION_URLS = urlpatterns
    FORM = form