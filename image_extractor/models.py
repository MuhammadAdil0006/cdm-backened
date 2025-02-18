from django.db import models

class ContentDataReport(models.Model):
    screenshot = models.FileField(upload_to="uploads/")
    ai_response = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"ExtractedData(id={self.id}, file={self.screenshot.name})"
