from celery import shared_task
from .models import ContentDataReport
from image_extractor.ai_services.gemini.tabular_data_extractor import GeminiTabularDataExtractor


@shared_task
def process_screenshot(content_data_report_id):
    try:
        instance = ContentDataReport.objects.get(id=content_data_report_id)
    except ContentDataReport.DoesNotExist:
        return f"ContentDataReport with ID {content_data_report_id} does not exist."
    
    gemini_tabular_data_extractor = GeminiTabularDataExtractor()
    file_path = instance.screenshot.path
    extracted_data = gemini_tabular_data_extractor.extract_data(file_path)
    print(extracted_data)
    instance.ai_response = extracted_data
    instance.save(update_fields=['ai_response'])

    return f"Data extraction complete for ContentDataReport ID {content_data_report_id}."
