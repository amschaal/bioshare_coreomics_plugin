from rest_framework import permissions
from dnaorder.models import Submission

class SubmissionStaffPermission(permissions.BasePermission):
    """Lab staff of the submission in the URL (and of the share being acted on)."""
    STAFF = [Submission.PERMISSION_ADMIN, Submission.PERMISSION_STAFF]
    def has_permission(self, request, view):
        # Checked for every action, including create/import_share, which never load an object.
        submission = Submission.objects.filter(pk=view.kwargs.get('submission_id')).first()
        return bool(submission) and submission.has_permission(request.user, self.STAFF, all=False)
    def has_object_permission(self, request, view, obj):
        return obj.submission.has_permission(request.user, self.STAFF, all=False)

class ListOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return view.action == 'list'
