from django.conf import settings
from django.db import models


class Resume(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resumes"
    )
    file = models.FileField(upload_to="resumes/")
    raw_text = models.TextField(blank=True, help_text="Extracted text, used as the source for skill parsing")
    extracted_skills = models.TextField(blank=True, help_text="Comma-separated skills found in the resume")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Resume for {self.user.username} ({self.uploaded_at:%Y-%m-%d})"
