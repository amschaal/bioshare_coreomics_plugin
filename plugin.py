from plugins import Plugin
from .urls import submission_urlpatterns, urlpatterns
from .forms import form
class BiosharePlugin(Plugin):
    ID = 'bioshare'
    URLS = urlpatterns
    SUBMISSION_URLS = submission_urlpatterns
    FORM = form