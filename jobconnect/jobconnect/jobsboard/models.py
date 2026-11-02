from django.conf import settings
from django.db import models


class JobPosting(models.Model):
    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="postings"
    )
    title = models.CharField(max_length=150)
    description = models.TextField()
    required_skills = models.TextField(help_text="Comma-separated, e.g. 'python, django, sql'")
    created_at = models.DateTimeField(auto_now_add=True)

    def skill_set(self) -> set[str]:
        return {s.strip().lower() for s in self.required_skills.split(",") if s.strip()}

    def __str__(self) -> str:
        return self.title


class Notification(models.Model):
    """A simple in-app alert, e.g. 'this new posting matches your profile'."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.CharField(max_length=255)
    posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.message
