"""Fires right after a new JobPosting is saved: scores it against every
seeker's profile and creates a Notification for anyone above the
threshold. This is the "real-time notifications" piece of the
proposal — simple and synchronous for now, easy to move onto a task
queue (Celery) later without changing matching.py at all.
"""
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Profile

from .matching import NOTIFY_THRESHOLD, match_score
from .models import JobPosting, Notification


@receiver(post_save, sender=JobPosting)
def notify_matching_candidates(sender, instance: JobPosting, created, **kwargs):
    if not created:
        return

    required = instance.skill_set()
    seekers = User.objects.filter(profile__role=Profile.Role.SEEKER)

    for seeker in seekers:
        score = match_score(seeker.profile.skill_set(), required)
        if score >= NOTIFY_THRESHOLD:
            Notification.objects.create(
                user=seeker,
                posting=instance,
                message=f"New match: '{instance.title}' is a {int(score * 100)}% skill match for you.",
            )
