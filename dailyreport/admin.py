from django.contrib import admin
from .models import DailyReport, WorkSession

@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'name', 'role')
    list_filter = ('date', 'user', 'role')
    search_fields = ('name', 'role', 'completed_tasks')

@admin.register(WorkSession)
class WorkSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'start_time', 'stop_time', 'duration_display')
    list_filter = ('date', 'user')
    search_fields = ('user__username',)

    def duration_display(self, obj):
        if obj.duration:
            # format duration nicely
            total_seconds = int(obj.duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        return "-"
    duration_display.short_description = "Duration"
