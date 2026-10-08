from rest_framework import serializers
from .models import SubmissionShare

class SubmissionShareSerializer(serializers.ModelSerializer):
    url = serializers.CharField(read_only=True)
    name = serializers.RegexField(regex=r'^[\w\d\s\'"\.!\?\-:,]+$',error_messages={'invalid': 'Name is required and may not contain any special characters.'})
    class Meta:
        model = SubmissionShare
        exclude = []
        read_only_fields = ('url', 'bioshare_id', 'id', 'submission')  # submission comes from the URL
