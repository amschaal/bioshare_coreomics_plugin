from django.conf import settings
CREATE_URL = settings.BIOSHARE_SETTINGS['URL'] + '/bioshare/api/shares/create/'
GET_URL = settings.BIOSHARE_SETTINGS['URL'] + '/bioshare/api/shares/{id}/'
VIEW_URL = settings.BIOSHARE_SETTINGS['URL'] + '/bioshare/view/{id}/'
GET_PERMISSIONS_URL = settings.BIOSHARE_SETTINGS['URL'] + '/bioshare/api/get_permissions/{id}'
SET_PERMISSIONS_URL = settings.BIOSHARE_SETTINGS['URL'] + '/bioshare/api/set_permissions/{id}'