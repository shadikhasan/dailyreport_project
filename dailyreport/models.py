# dailyreport/models.py

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

