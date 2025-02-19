from django.db import models

class ContentDataReport(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    ai_response = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return f"ContentDataReport(id={self.id}, name={self.name})"

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