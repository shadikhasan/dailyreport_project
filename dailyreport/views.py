from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.utils.timezone import now
from django.http import JsonResponse
from django.db.models import F, ExpressionWrapper, DurationField, Sum
from django.db.models.functions import ExtractWeek, ExtractMonth, ExtractYear
from datetime import timedelta
from collections import OrderedDict, defaultdict

from .models import DailyReport, WorkSession
from .forms import DailyReportForm

# --- Registration ---
from django.contrib.auth.forms import UserCreationForm

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


# --- Home redirect ---
def home_redirect(request):
    return redirect('dashboard')


# --- Dashboard ---
@login_required
def dashboard_view(request):
    user = request.user

    total_my_reports = DailyReport.objects.filter(user=user).count()
    latest_report = DailyReport.objects.filter(user=user).order_by('-date').first()

    today = timezone.now().date()
    today_sessions = WorkSession.objects.filter(user=user, date=today)

    # Total duration of finished sessions
    finished_sessions = today_sessions.filter(stop_time__isnull=False).annotate(
        session_duration=ExpressionWrapper(
            F('stop_time') - F('start_time'),
            output_field=DurationField()
        )
    )
    total_finished_duration = finished_sessions.aggregate(total=Sum('session_duration'))['total'] or timedelta()

    # Ongoing session duration
    ongoing_session = today_sessions.filter(stop_time__isnull=True).first()
    ongoing_duration = timedelta()
    if ongoing_session:
        ongoing_duration = timezone.now() - ongoing_session.start_time

    # Sum total duration
    total_duration = total_finished_duration + ongoing_duration

    return render(request, 'dashboard.html', {
        'total_my_reports': total_my_reports,
        'latest_report': latest_report,
        'today_sessions': today_sessions,
        'total_duration': total_duration,
    })


# --- Daily Report CRUD ---
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
def my_report_detail(request, pk):
    report = get_object_or_404(DailyReport, pk=pk, user=request.user)
    return render(request, 'my_report_detail.html', {'report': report})

@login_required
def all_reports_page(request):
    reports = DailyReport.objects.all().order_by('-date')
    return render(request, 'all_reports.html', {'reports': reports})

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

@login_required
def delete_report(request, pk):
    report = get_object_or_404(DailyReport, pk=pk, user=request.user)
    if request.method == 'POST':
        report.delete()
        return redirect('my-reports-page')
    return render(request, 'delete_report.html', {'report': report})

@login_required
def report_detail(request, pk):
    report = get_object_or_404(DailyReport, pk=pk)
    return render(request, 'report_detail.html', {'report': report})


# --- Weekly Reports Grouped ---
@login_required
def weekly_reports_page(request):
    user = request.user
    reports = DailyReport.objects.filter(user=user).order_by('-date')
    grouped = defaultdict(list)
    for report in reports:
        iso_year, iso_week, _ = report.date.isocalendar()
        grouped[(iso_year, iso_week)].append(report)
    weekly_reports = OrderedDict(sorted(grouped.items(), reverse=True))
    return render(request, "weekly_reports.html", {"weekly_reports": weekly_reports})


# --- Work Session Start/Stop ---
@csrf_exempt
@login_required
def start_work_session(request):
    if request.method == 'POST':
        if WorkSession.objects.filter(user=request.user, stop_time__isnull=True).exists():
            return JsonResponse({'error': 'Session already in progress'}, status=400)
        WorkSession.objects.create(user=request.user, start_time=timezone.now())
        return JsonResponse({'message': 'Work session started!'})

@csrf_exempt
@login_required
def stop_work_session(request):
    if request.method == 'POST':
        session = WorkSession.objects.filter(user=request.user, stop_time__isnull=True).first()
        if session:
            session.stop_time = timezone.now()
            session.save()
            return JsonResponse({'message': 'Session stopped!', 'duration': str(session.duration)})
        return JsonResponse({'error': 'No active session'}, status=400)


# --- User Status / Work Hours Summaries ---
from django.contrib.auth import get_user_model

def get_users_with_status(month=None, year=None):
    User = get_user_model()
    users = User.objects.all()
    today = now().date()
    if not month:
        month = today.month
    if not year:
        year = today.year

    start_of_month = today.replace(month=month, year=year, day=1)
    if month == 12:
        end_of_month = start_of_month.replace(year=year + 1, month=1, day=1) - timedelta(days=1)
    else:
        end_of_month = start_of_month.replace(month=month + 1, day=1) - timedelta(days=1)

    user_status = []
    for user in users:
        today_sessions = WorkSession.objects.filter(user=user, start_time__date=today)
        total_duration_today = timedelta()
        for session in today_sessions:
            stop = session.stop_time or now()
            total_duration_today += (stop - session.start_time)
        month_sessions = WorkSession.objects.filter(
            user=user,
            start_time__date__gte=start_of_month,
            start_time__date__lte=end_of_month
        )
        total_duration_month = timedelta()
        for session in month_sessions:
            stop = session.stop_time or now()
            total_duration_month += (stop - session.start_time)
        active_session = today_sessions.filter(stop_time__isnull=True).first()
        # If using a custom user model with .role, use user.role
        # Otherwise, get role from latest report
        latest_report = DailyReport.objects.filter(user=user).order_by('-date').first()
        role = getattr(user, 'role', None) or (latest_report.role if latest_report else '-')
        user_status.append({
            'user': user,
            'role': role,
            'is_working': bool(active_session),
            'start_time': active_session.start_time if active_session else None,
            'total_working_time_today': str(total_duration_today).split('.')[0],
            'total_working_time_month': str(total_duration_month).split('.')[0],
        })
    return user_status

@login_required
def users_working_status(request):
    try:
        month = int(request.GET.get('month', now().month))
        year = int(request.GET.get('year', now().year))
    except ValueError:
        month = now().month
        year = now().year

    user_status = get_users_with_status(month=month, year=year)
    current_year = now().year
    current_month = now().month

    return render(request, 'users_working_status.html', {
        'user_status': user_status,
        'selected_month': month,
        'selected_year': year,
        'current_year': current_year,
        'current_month': current_month,
    })


# --- Work Hours Summary ---
@login_required
def work_hours_summary(request, period):
    user = request.user
    sessions = WorkSession.objects.filter(user=user, stop_time__isnull=False)
    sessions = sessions.annotate(
        duration=ExpressionWrapper(
            F('stop_time') - F('start_time'),
            output_field=DurationField()
        )
    )

    if period == 'weekly':
        summary_data = sessions.values(
            year=ExtractYear('start_time'),
            week=ExtractWeek('start_time')
        ).annotate(
            total_duration=Sum('duration')
        ).order_by('-year', '-week')
        for entry in summary_data:
            total_seconds = entry['total_duration'].total_seconds()
            entry['formatted_duration'] = str(timedelta(seconds=total_seconds))
        context = {
            'summary_data': summary_data,
            'period': 'weekly',
        }
    elif period == 'monthly':
        summary_data = sessions.values(
            year=ExtractYear('start_time'),
            month=ExtractMonth('start_time')
        ).annotate(
            total_duration=Sum('duration')
        ).order_by('-year', '-month')
        for entry in summary_data:
            total_seconds = entry['total_duration'].total_seconds()
            entry['formatted_duration'] = str(timedelta(seconds=total_seconds))
        context = {
            'summary_data': summary_data,
            'period': 'monthly',
        }
    else:
        return render(request, '404.html', status=404)
    
    # All completed sessions for the user
    finished_sessions = WorkSession.objects.filter(user=user, stop_time__isnull=False).annotate(
        duration=ExpressionWrapper(
            F('stop_time') - F('start_time'),
            output_field=DurationField()
        )
    )

    # Total duration of all completed sessions
    total_finished_duration = finished_sessions.aggregate(total=Sum('duration'))['total'] or timedelta()

    # Ongoing session (not finished)
    ongoing_session = WorkSession.objects.filter(user=user, stop_time__isnull=True).first()
    ongoing_duration = timedelta()
    if ongoing_session:
        ongoing_duration = timezone.now() - ongoing_session.start_time

    # Total (finished + ongoing)
    total_duration_all_time = total_finished_duration + ongoing_duration

    context['total_duration_all_time'] = total_duration_all_time
    
    return render(request, 'work_hours_summary.html', context)
