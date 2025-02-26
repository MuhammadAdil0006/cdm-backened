from celery import shared_task
from .models import ContentDataReport, ContentDataReportImage
from image_extractor.ai_services.gemini.tabular_data_extractor import GeminiTabularDataExtractor

@shared_task
def process_screenshot(content_data_report_id):
    try:
        instance = ContentDataReport.objects.get(id=content_data_report_id)
    except ContentDataReport.DoesNotExist:
        return f"ContentDataReport with ID {content_data_report_id} does not exist."
    
    gemini_tabular_data_extractor = GeminiTabularDataExtractor()
    related_images = instance.content_data_report_images.filter(screenshot_type=ContentDataReportImage.PARTIAL)

    if not related_images.exists():
        return f"No images found for ContentDataReport ID {content_data_report_id}."
    file_paths = [related_image.screenshot.path for related_image in related_images]

    instance.ai_response = gemini_tabular_data_extractor.extract_data(file_paths)
    instance.ai_response_generation_status = ContentDataReport.AI_Response_States.SUCCESS
    print(instance.ai_response)
    instance.save(update_fields=['ai_response', 'ai_response_generation_status'])

    return f"Data extraction complete for ContentDataReport ID {content_data_report_id}."
