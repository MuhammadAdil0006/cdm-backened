from rest_framework import serializers
from image_extractor.models import ContentDataReport


class ContentDataReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentDataReport
        fields = ["id", "screenshot", "ai_response"]

