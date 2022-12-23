from django.db import models
# from django.db.models.signals import post_save, pre_save
import urllib
import json
# from bioshare.utils import get_real_files, get_symlinks, remove_sub_paths
from .plugin import CREATE_URL, VIEW_URL, GET_PERMISSIONS_URL, SET_PERMISSIONS_URL
from django.conf import settings
from dnaorder.models import Lab, Submission
from .requests import bioshare_post, bioshare_get, create_share

class BioshareAccount(models.Model):
    lab = models.OneToOneField(Lab, related_name="bioshare_account", primary_key=True, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    def __unicode__(self):
        return 'Bioshare account: %s'%self.lab.name
    def create_share(self, name, description=None):
#         @todo: replace with real API call
#         import string, random
#         return ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(15))
        """
newConditions = {"con1":40, "con2":20, "con3":99, "con4":40, "password":"1234"} 
params = json.dumps(newConditions).encode('utf8')
req = urllib.request.Request(conditionsSetURL, data=params,
                             headers={'content-type': 'application/json'})
response = urllib.request.urlopen(req)
        """
        description = description or 'Genome Center LIMS generated share'
        filesystem = settings.BIOSHARE_SETTINGS['DEFAULT_FILESYSTEM']
        params = {"name":name,"notes":description,"filesystem":filesystem,'read_only':False}
        return bioshare_post(CREATE_URL, self.auth_token, params)['id']
#         req = urllib.request.Request(CREATE_URL, data=params)
# #         req.add_data(params)
#         req.add_header('Content-Type', 'application/json')
#         req.add_header('Authorization', 'Token %s'%self.auth_token)
#         
#         try:
#             response = urllib.request.urlopen(req)
#             if response.getcode() == 200:
#                 data = json.load(response)
#                 return data['id']
#             else:
#                 raise Exception('Unable to create share')
#         except urllib.request.HTTPError as e:
#             error_message = e.read()
# #             print error_message
#             raise Exception('Unable to create share')

class SubmissionShare(models.Model):
    ADMIN_PERMISSIONS = ["view_share_files","download_share_files","write_to_share","delete_share_files","admin"]
    VIEWER_PERMISSIONS = ["view_share_files","download_share_files"]
    id = models.CharField(max_length=30, primary_key=True)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
#     labshare = models.ForeignKey(LabShare)
    name = models.CharField(max_length=50)
    notes = models.TextField(null=True)
    bioshare_id = models.CharField(max_length=15,null=True,blank=True)
    sub_folder = models.CharField(max_length=100, null=True, blank=True)
#     class Meta:
#         unique_together = (('labshare','folder'),('project','labshare'))
    def save(self, *args, **kwargs):
        if not self.bioshare_id:
            name = self.name or '{}: {}'.format('{}, {}'.format(self.submission.pi_last_name, self.submission.pi_first_name),self.submission.internal_id)
            notes = self.notes or 'Generated from {}'.format(self.submission.internal_id)
            self.bioshare_id = create_share(self.submission.lab.plugins['bioshare']['private']['token'], name, notes)
#             self.bioshare_id = self.submission.lab.bioshare_account.create_share('{}: {}'.format('{}, {}'.format(self.submission.pi_last_name, self.submission.pi_first_name),self.submission.internal_id), 'Generated from {}'.format(self.submission.internal_id))
        if not self.id:
            self.id = '{}_{}'.format(self.submission.pk, self.bioshare_id)
        instance = super(SubmissionShare, self).save(*args, **kwargs)
        if settings.BIOSHARE_SETTINGS.get('AUTO_SHARE_PARTICIPANTS', False):
            self.share_with_participants()
        return instance
        
    @property
    def url(self):
        return VIEW_URL.format(id=self.bioshare_id)
    def set_permissions(self, perms=None):
#         if not perms:
#             perms = {"test": True, "groups": {}, "users":dict([(p.email,["view_share_files","download_share_files","write_to_share","delete_share_files","admin"]) for p in self.submission.participants.all()]), "email":True}
#         print('perms', perms)
#       perms = {"users":{"jdoe@domain.com":["view_share_files","download_share_files","write_to_share","delete_share_files","admin"]},"groups":{"1":["view_share_files","download_share_files","write_to_share"]},"email":true}
        return bioshare_post(SET_PERMISSIONS_URL.format(id=self.bioshare_id), self.submission.lab.plugins['bioshare']['private']['token'], perms)
    def share_with_participants(self):
        perms = {"groups": {}, "users":dict([(p.email, self.ADMIN_PERMISSIONS) for p in self.submission.participants.all()]), "email":True}
        return self.set_permissions(perms)
    def share(self, contacts=False):
        emails = [self.submission.email, self.submission.pi_email]
        if contacts:
            emails += [c.email for c in self.submission.contacts.all()]
        perms = {"groups": {}, "users":dict([(email,self.VIEWER_PERMISSIONS) for email in emails]), "email":True}
        return self.set_permissions(perms)
    def get_permissions(self):
        return bioshare_get(GET_PERMISSIONS_URL.format(id=self.bioshare_id), self.submission.lab.plugins['bioshare']['private']['token'])
# def create_submission_share_directory(sender,instance,**kwargs):
#     if hasattr(instance, 'id'):
#         try:
#             old = sender.objects.get(id=instance.id)
#             old_directory = old.directory()
#             new_directory = instance.directory()
#             if old_directory != new_directory and os.path.isdir(old_directory):
#                 shutil.move(old_directory, new_directory)
#         except:
#             pass
#     if not os.path.exists(instance.directory()):
#         os.makedirs(instance.directory())
# pre_save.connect(create_project_share_directory, ProjectShare)
