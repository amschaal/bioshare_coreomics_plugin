from .api import SubmissionShareViewSet, ShareViewSet

from rest_framework import routers

submission_router = routers.DefaultRouter()
submission_router.register(r'submission_shares', SubmissionShareViewSet,'SubmissionShare')

router = routers.DefaultRouter()
router.register(r'shares', ShareViewSet,'Share')

submission_urlpatterns = submission_router.urls
urlpatterns = router.urls