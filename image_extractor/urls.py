from django.urls import path

from . import views

urlpatterns = [
    path("extract-data/", views.ContentDataReportView.as_view(), name="extract-data"),
    path("reports/", views.content_data_report_list, name="content_data_report_list"),
    path("report/<int:pk>/", views.content_data_report_detail, name="content_data_report_detail"),
]
