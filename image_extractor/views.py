from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import ContentDataReport
from .serializers import ContentDataReportSerializer
from .tasks import process_screenshot


class ContentDataReportView(generics.CreateAPIView):
    queryset = ContentDataReport.objects.all()
    serializer_class = ContentDataReportSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        # Check if 'file' is in request.FILES
        if 'image' not in request.FILES:
            return Response(
                {"error": "No file provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data={"screenshot": request.FILES["image"]})
        if serializer.is_valid():
            instance = serializer.save()
            process_screenshot.delay(instance.id)
            return Response(
                {
                    "message": "File uploaded successfully!",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
