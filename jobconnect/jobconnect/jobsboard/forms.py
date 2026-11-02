from django import forms

from .models import JobPosting


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ["title", "description", "required_skills"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            "required_skills": forms.TextInput(attrs={"placeholder": "python, django, sql"}),
        }
