# dailyreport/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('reports/', DailyReportListCreateAPIView.as_view(), name='daily-report-list-create'),
    path('reports/mine/', MyReportsAPIView.as_view(), name='my-daily-reports'),
    
    # Template views
    path('submit/', submit_report, name='submit-report-page'),
    path('reports/my/', my_reports_page, name='my-reports-page'),
    path('reports/all/', all_reports_page, name='all-reports-page'),
]
