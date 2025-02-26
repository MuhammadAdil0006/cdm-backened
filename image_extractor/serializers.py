from rest_framework import serializers
from image_extractor.models import ContentDataReport, ContentDataReportImage

class ContentDataReportSerializer(serializers.ModelSerializer):
    ai_response_generation_status = serializers.CharField(source='get_ai_response_generation_status_display', read_only=True)

    class Meta:
        model = ContentDataReport
        fields = ["id", "name", "recording", "ai_response", "ai_response_generation_status"]
