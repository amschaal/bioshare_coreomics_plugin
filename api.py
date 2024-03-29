from rest_framework import viewsets, status, mixins, exceptions, permissions as drf_permissions
from dnaorder.models import Submission

from plugins import plugin_submission_decorator
from plugins.bioshare.config import GET_PERMISSIONS_URL
from plugins.bioshare.requests import bioshare_get, get_share, parse_share_id
from .permissions import ListOnlyPermission, SubmissionStaffPermission
from .models import SubmissionShare, BioshareAccount
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .serializers import SubmissionShareSerializer,\
    BioshareAccountSerializer
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication,\
    TokenAuthentication

# mixins.CreateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.ListModelMixin,
#                    mixins.DestroyModelMixin,
#                    GenericViewSet

class SubmissionShareViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionShareSerializer
    model = SubmissionShare
    filterset_fields = ('submission',)
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [ListOnlyPermission|SubmissionStaffPermission]
    queryset = SubmissionShare.objects.all()
    def get_permissions(self):
        return super().get_permissions()
    def get_queryset(self):
        # print('get_queryset',self.kwargs)
        self.submission_id = self.kwargs.get('submission_id')
        self.plugin_id = self.kwargs.get('plugin_id')
        self.submission = Submission.objects.get(id=self.submission_id)
        return SubmissionShare.objects.filter(submission=self.submission)
    @action(detail=True, methods=['GET'], permission_classes=[SubmissionStaffPermission])
    # @plugin_submission_decorator(permissions=['VIEW'], all=True)
    def permissions(self, request, pk=None, submission_id=None, plugin_id=None):
        obj = self.get_object()
        return Response({'permissions': obj.get_permissions()})
    @action(detail=True, methods=['POST'], permission_classes=[SubmissionStaffPermission])
    def share_with_participants(self, request, pk=None, submission_id=None, plugin_id=None):
        obj = self.get_object()
        email = request.data.get('email', False)
        return Response({'permissions': obj.share_with_participants(email=email)})
    @action(detail=True, methods=['POST'], permission_classes=[SubmissionStaffPermission])
    def share(self, request, pk=None, submission_id=None, plugin_id=None):
        obj = self.get_object()
        email = request.data.get('email', False)
        return Response({'permissions': obj.share(contacts=True, email=email)})
    # def list(self, request, *args, permission_classes=[drf_permissions.AllowAny], **kwargs):
    #     # if 'submission' not in request.query_params:
    #     #     return Response({'status':'error', 'message': 'You must provide a submission id as an argument (submission=<submission_id>).'},status=403)
    #     return viewsets.ModelViewSet.list(self, request, *args, **kwargs)
    @action(detail=False, methods=['POST'], permission_classes=[SubmissionStaffPermission])
    def import_share(self, request, submission_id=None, plugin_id=None):
        url = request.data.get('url')
        share_id = parse_share_id(url)
        if not share_id:
            raise exceptions.NotAcceptable('Bad URL.  Ensure that the URL contains the 15 digit alphanumeric share ID.')
        submission = Submission.objects.get(id=submission_id)
        try:
            share = get_share(submission.lab.plugins['bioshare']['private']['token'], share_id)#bioshare_get(GET_PERMISSIONS_URL.format(id=share_id), submission.lab.plugins['bioshare']['private']['token'])
            obj = SubmissionShare(bioshare_id = share_id, name=share['name'], notes=share['notes'], submission=submission)
            obj.save()
            serializer = self.get_serializer(obj)
            return Response(serializer.data)
        except Exception as e:
            raise exceptions.APIException('Unable to import share. Exception: '+ str(e))
#     def create(self, request, *args, **kwargs):
#         return viewsets.ModelViewSet.create(self, request, *args, **kwargs)
#     def create(self, request, *args, **kwargs):
#         try:    
#             project = Project.objects.get(id=request.data.get('project'))
#     #         labshare, created = LabShare.objects.get_or_create(lab=project.lab,group=project.group) 
#     #         data = {'project':request.data.get('project'),'folder':,'labshare':labshare.id}
#             project_share = ProjectShare.objects.create(project=project)
#             serializer = self.get_serializer(project_share)
#     #         print "LABSHARE"
#     #         serializer.is_valid(raise_exception=True)
#     #         self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#         except Exception, e:
#             return Response({'status':'error','message':e.message},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     @action(detail=True, methods=['post'])
#     def unlink_paths(self, request, pk=None):
#         obj = self.get_object()
#         paths = request.data.get('paths',[])
#         stats = obj.unlink_paths(paths)
#         return Response({'status': 'success','stats':stats,'symlinks':obj.symlinks(recalculate=True)})
#     @detail_route(methods=['post'])
#     def set_paths(self, request, pk=None):
#         obj = self.get_object()
#         paths = request.data.get('paths',[])
#         stats = obj.set_paths(paths)
#         return Response({'status': 'success','stats':stats,'symlinks':obj.symlinks(recalculate=True)})

class BioshareAccountViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    serializer_class = BioshareAccountSerializer
    model = BioshareAccount
    queryset = BioshareAccount.objects.all()