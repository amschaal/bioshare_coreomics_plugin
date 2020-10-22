from rest_framework import viewsets, status, mixins
from bioshare.models import SubmissionShare, BioshareAccount
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from bioshare.serializers import SubmissionShareSerializer,\
    BioshareAccountSerializer
from rest_framework.decorators import action

class SubmissionShareViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    serializer_class = SubmissionShareSerializer
    model = SubmissionShare
#     filter_fields = ('submission',)
#     permission_classes = []
    queryset = SubmissionShare.objects.all()
    @action(detail=True, methods=['GET'], permission_classes=[])
    def permissions(self, request, pk=None):
        obj = self.get_object()
        return Response({'permissions': obj.get_permissions()})
    @action(detail=True, methods=['POST'])
    def set_permissions(self, request, pk=None):
        obj = self.get_object()
        perms = request.data
        print('set perms', perms)
        return Response({'permissions': obj.set_permissions()})
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