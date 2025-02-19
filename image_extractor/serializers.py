from rest_framework import serializers
from image_extractor.models import ContentDataReport, ContentDataReportImage

class ContentDataReportSerializer(serializers.ModelSerializer):
    full_length_screenshot = serializers.SerializerMethodField()

    class Meta:
        model = ContentDataReport
        fields = ["id", "name", "full_length_screenshot", "ai_response"]

    def get_full_length_screenshot(self, obj):
        full_screenshot = obj.content_data_report_images.filter(screenshot_type=ContentDataReportImage.FULL).first()
        return full_screenshot.screenshot.url if full_screenshot else None
