from django.conf import settings
from django.db import models


class Profile(models.Model):
    """Extends the built-in User with a role (seeker/employer) and a
    comma-separated skill list that the matching logic reads from.

    For a job seeker, `skills` is filled in automatically when they
    upload a resume (see resumes.utils.extract_skills). For an
    employer it is left blank.
    """

    class Role(models.TextChoices):
        SEEKER = "seeker", "Job Seeker"
        EMPLOYER = "employer", "Employer"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    role = models.CharField(max_length=10, choices=Role.choices)
    headline = models.CharField(max_length=150, blank=True, help_text="e.g. 'Final-year CS student' or 'Hiring manager, Acme Corp'")
    github_username = models.CharField(max_length=100, blank=True, help_text="Optional — used to enrich the skill profile from public repos")
    skills = models.TextField(blank=True, help_text="Comma-separated skills, auto-filled from resume parsing")

    def skill_set(self) -> set[str]:
        return {s.strip().lower() for s in self.skills.split(",") if s.strip()}

    def __str__(self) -> str:
        return f"{self.user.username} ({self.get_role_display()})"
