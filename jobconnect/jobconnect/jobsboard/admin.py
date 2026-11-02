from django.contrib import admin

from .models import JobPosting, Notification


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ("title", "employer", "required_skills", "created_at")
    search_fields = ("title", "required_skills")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "posting", "is_read", "created_at")
    list_filter = ("is_read",)
