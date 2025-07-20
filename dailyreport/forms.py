from django import forms
from .models import DailyReport

class DailyReportForm(forms.ModelForm):
    class Meta:
        model = DailyReport
        exclude = ['user']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your role'}),
            'completed_tasks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tasks completed'}),
            'in_progress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tasks in progress'}),
            'blockers': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Any blockers?'}),
            'plan_tomorrow': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Plans for tomorrow'}),
            'links': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Relevant links'}),
        }
