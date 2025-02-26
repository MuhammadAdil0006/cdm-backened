from rest_framework import serializers
from image_extractor.models import ContentDataReport, ContentDataReportImage

class ContentDataReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContentDataReport
        fields = ["id", "name", "recording", "ai_response"]
