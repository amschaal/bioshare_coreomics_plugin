from plugins import Plugin
from .urls import urlpatterns
from .forms import form
class BiosharePlugin(Plugin):
    ID = 'bioshare'
    SUBMISSION_URLS = urlpatterns
    FORM = form