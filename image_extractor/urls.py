from django.urls import path

from . import views

urlpatterns = [
    path("extract-data/", views.ContentDataReportView.as_view(), name="extract-data"),
]
