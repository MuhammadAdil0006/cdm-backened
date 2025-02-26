from django.db import models
from django.utils.translation import gettext_lazy as _

class ContentDataReport(models.Model):
    class AI_Response_States(models.IntegerChoices):
        IN_PROGRESS = 0, _('IN_PROGRESS')
        SUCCESS = 1, _('SUCCESS')
    name = models.CharField(max_length=255, blank=True, null=True)
    ai_response = models.JSONField(blank=True, null=True)
    recording = models.FileField(upload_to="uploads/recordings/", blank=True, null=True)
    ai_response_generation_status = models.PositiveSmallIntegerField(choices=AI_Response_States.choices, default=AI_Response_States.IN_PROGRESS)

    def __str__(self):
        return f"ContentDataReport(id={self.id}, name={self.name})"
    
    def get_ai_response_generation_status_display(self):
        return self.AI_Response_States(self.ai_response_generation_status).label

class ContentDataReportImage(models.Model):
    FULL = 1
    PARTIAL = 2
    SCREENSHOT_TYPE_CHOICES = [
        (FULL, "Full"),
        (PARTIAL, "Partial"),
    ]
    
    screenshot = models.FileField(upload_to="uploads/screenshots/")
    screenshot_type = models.PositiveSmallIntegerField(choices=SCREENSHOT_TYPE_CHOICES)
    content_data_report = models.ForeignKey(ContentDataReport, on_delete=models.CASCADE, related_name="content_data_report_images")
    
    def __str__(self):
        return f"Screenshot(id={self.id}, type={self.get_screenshot_type_display()}, report_id={self.content_data_report.id})"
