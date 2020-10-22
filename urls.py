# from django.conf.urls import include, url
from bioshare.api import SubmissionShareViewSet, BioshareAccountViewSet

from rest_framework import routers
# from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'submission_shares', SubmissionShareViewSet,'SubmissionShare')
router.register(r'accounts', BioshareAccountViewSet,'BioshareAccount')

# urlpatterns = [
#     path(r'^api/', include(router.urls)),
# ]
urlpatterns = router.urls