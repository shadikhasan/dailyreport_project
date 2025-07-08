# dailyreport/forms.py

from django import forms
from .models import DailyReport

class DailyReportForm(forms.ModelForm):
    class Meta:
        model = DailyReport
        fields = ['date', 'name', 'role', 'completed_tasks', 'in_progress', 'blockers', 'plan_tomorrow', 'links']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Select date',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
            }),
            'role': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your role in the project',
            }),
            'completed_tasks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Tasks you completed today',
            }),
            'in_progress': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Tasks currently in progress',
            }),
            'blockers': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Any blockers or issues',
            }),
            'plan_tomorrow': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Plan for tomorrow',
            }),
            'links': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Relevant links (e.g. Jira, GitHub)',
            }),
        }
