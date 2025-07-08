# dailyreport/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import DailyReport
from django.contrib.auth import login  # ✅ this is the missing import
from .serializers import DailyReportSerializer

class DailyReportListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        reports = DailyReport.objects.all().order_by('-date')
        serializer = DailyReportSerializer(reports, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DailyReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # set user from request
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyReportsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        reports = DailyReport.objects.filter(user=request.user).order_by('-date')
        serializer = DailyReportSerializer(reports, many=True)
        return Response(serializer.data)


# dailyreport/views.py (add below your APIViews)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import DailyReport
from .forms import DailyReportForm

@login_required
def submit_report(request):
    if request.method == 'POST':
        form = DailyReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            return redirect('my-reports-page')
    else:
        form = DailyReportForm()
    return render(request, 'submit_report.html', {'form': form})

@login_required
def my_reports_page(request):
    reports = DailyReport.objects.filter(user=request.user).order_by('-date')
    return render(request, 'my_reports.html', {'reports': reports})

@login_required
def all_reports_page(request):
    reports = DailyReport.objects.all().order_by('-date')
    return render(request, 'all_reports.html', {'reports': reports})



from django.contrib.auth.forms import UserCreationForm
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after register
            return redirect('submit-report-page')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    from .models import DailyReport

    user = request.user
    total_my_reports = DailyReport.objects.filter(user=user).count()
    latest_report = DailyReport.objects.filter(user=user).order_by('-date').first()

    context = {
        'total_my_reports': total_my_reports,
        'latest_report': latest_report,
    }
    return render(request, 'dashboard.html', context)
