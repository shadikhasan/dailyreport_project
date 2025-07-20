# dailyreport/models.py
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class DailyReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    completed_tasks = models.TextField()
    in_progress = models.TextField(blank=True)
    blockers = models.TextField(blank=True)
    plan_tomorrow = models.TextField()
    links = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} - {self.name}"


class WorkSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    start_time = models.DateTimeField()
    stop_time = models.DateTimeField(null=True, blank=True)

    @property
    def duration(self):
        if self.start_time and self.stop_time:
            return self.stop_time - self.start_time
        elif self.start_time:
            return timezone.now() - self.start_time
        return None

    def __str__(self):
        return f"{self.user.username}: {self.start_time} - {self.stop_time or 'Ongoing'}"