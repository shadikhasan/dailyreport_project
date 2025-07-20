from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import DailyReport
from .forms import DailyReportForm

from django.shortcuts import redirect

def home_redirect(request):
    return redirect('dashboard')


# --- Registration ---
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# --- Dashboard ---
@login_required
def dashboard_view(request):
    user = request.user
    total_my_reports = DailyReport.objects.filter(user=user).count()
    latest_report = DailyReport.objects.filter(user=user).order_by('-date').first()
    return render(request, 'dashboard.html', {
        'total_my_reports': total_my_reports,
        'latest_report': latest_report,
    })

# --- Submit/Create Daily Report ---
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

# --- List My Reports ---
@login_required
def my_reports_page(request):
    reports = DailyReport.objects.filter(user=request.user).order_by('-date')
    return render(request, 'my_reports.html', {'reports': reports})

@login_required
def my_report_detail(request, pk):
    from django.shortcuts import get_object_or_404
    report = get_object_or_404(DailyReport, pk=pk, user=request.user)
    return render(request, 'my_report_detail.html', {'report': report})


# --- List All Reports ---
@login_required
def all_reports_page(request):
    reports = DailyReport.objects.all().order_by('-date')
    return render(request, 'all_reports.html', {'reports': reports})

# --- Edit Report ---
@login_required
def edit_report(request, pk):
    report = get_object_or_404(DailyReport, pk=pk, user=request.user)
    if request.method == 'POST':
        form = DailyReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('my-reports-page')
    else:
        form = DailyReportForm(instance=report)
    return render(request, 'edit_report.html', {'form': form, 'report': report})

# --- Delete Report ---
@login_required
def delete_report(request, pk):
    report = get_object_or_404(DailyReport, pk=pk, user=request.user)
    if request.method == 'POST':
        report.delete()
        return redirect('my-reports-page')
    return render(request, 'delete_report.html', {'report': report})

@login_required
def report_detail(request, pk):
    from django.shortcuts import get_object_or_404
    report = get_object_or_404(DailyReport, pk=pk)
    return render(request, 'report_detail.html', {'report': report})


@login_required
def weekly_reports_page(request):
    user = request.user
    # Query all reports for this user, newest first
    reports = DailyReport.objects.filter(user=user).order_by('-date')
    
    # Group reports by ISO week (year, week)
    from collections import OrderedDict, defaultdict
    grouped = defaultdict(list)
    for report in reports:
        iso_year, iso_week, _ = report.date.isocalendar()
        grouped[(iso_year, iso_week)].append(report)

    # Sort weeks descending (most recent first)
    weekly_reports = OrderedDict(
        sorted(grouped.items(), reverse=True)
    )
    
    context = {
        "weekly_reports": weekly_reports
    }
    return render(request, "weekly_reports.html", context)