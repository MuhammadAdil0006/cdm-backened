from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import ContentDataReport, ContentDataReportImage
from .serializers import ContentDataReportSerializer
from .tasks import process_screenshot
from django.shortcuts import render, get_object_or_404
import json


class ContentDataReportView(generics.CreateAPIView):
    queryset = ContentDataReport.objects.all()
    serializer_class = ContentDataReportSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        if 'screenshots_in_parts' not in request.FILES and 'full_length_screenshot' not in request.FILES:
            return Response(
                {"error": "No files provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        content_data_report = ContentDataReport.objects.create(name=request.data.get("name", ""))
        for file in reversed(request.FILES.getlist("screenshots_in_parts")):
            ContentDataReportImage.objects.create(
                content_data_report=content_data_report,
                screenshot=file,
                screenshot_type=ContentDataReportImage.PARTIAL
            )

        full_screenshot = request.FILES.get("full_length_screenshot")
        if full_screenshot:
            ContentDataReportImage.objects.create(
                content_data_report=content_data_report,
                screenshot=full_screenshot,
                screenshot_type=ContentDataReportImage.FULL
            )
        process_screenshot.delay(content_data_report.id)
        serializer = self.get_serializer(content_data_report)
        return Response(
            {
                "message": "Files uploaded successfully!",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


def content_data_report_list(request):
    reports = ContentDataReport.objects.all()
    return render(request, "image_extractor/content_data_report_list.html", {"reports": reports})


def content_data_report_detail(request, pk):
    instance = get_object_or_404(ContentDataReport, pk=pk)
    serializer = ContentDataReportSerializer(instance)

    # Extract data from the serializer
    serialized_data = serializer.data
    screenshot_url = serialized_data.get("full_length_screenshot")
    ai_response = serialized_data.get("ai_response")

    # Handle AI response parsing
    if isinstance(ai_response, str):
        try:
            ai_data = json.loads(ai_response)  # Convert JSON string to Python list/dict
        except json.JSONDecodeError:
            ai_data = []
    elif isinstance(ai_response, (list, dict)):  # Ensure ai_response can be iterated over
        ai_data = ai_response
    else:
        ai_data = []

    return render(
        request, 
        "image_extractor/content_data_report_detail.html", 
        {"data": ai_data, "screenshot_url": screenshot_url}
    )
