from rest_framework import permissions
from dnaorder.models import Submission

class SubmissionStaffPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.submission.has_permission(request.user, permissions=[Submission.PERMISSION_ADMIN,Submission.PERMISSION_STAFF], all=False)

class ListOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return view.action == 'list'
