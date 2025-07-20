from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_view, name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('submit/', submit_report, name='submit-report-page'),
    path('reports/my/', my_reports_page, name='my-reports-page'),
    path('reports/my/<int:pk>/', my_report_detail, name='my-report-detail-page'),
    path('reports/all/', all_reports_page, name='all-reports-page'),
    path('reports/<int:pk>/', report_detail, name='report-detail-page'),
    path('reports/<int:pk>/edit/', edit_report, name='edit-report-page'),
    path('reports/<int:pk>/delete/', delete_report, name='delete-report-page'),
    
    path('reports/weekly/', weekly_reports_page, name='weekly-reports-page'),
]
