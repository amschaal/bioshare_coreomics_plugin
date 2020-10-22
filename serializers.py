from rest_framework import serializers
from bioshare.models import SubmissionShare, BioshareAccount

class SubmissionShareSerializer(serializers.ModelSerializer):
    url = serializers.CharField(read_only=True)
    class Meta:
        model = SubmissionShare
        exclude = []
        read_only_fields = ('url', 'bioshare_id')

class BioshareAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BioshareAccount
        exclude = []
