from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Profile

from .forms import JobPostingForm
from .matching import rank_postings_for
from .models import JobPosting, Notification


def posting_list(request):
    """For a logged-in seeker, show postings ranked by match score.
    Otherwise (employer or anonymous visitor), show the plain list."""
    postings = JobPosting.objects.select_related("employer").order_by("-created_at")

    ranked = None
    if request.user.is_authenticated and getattr(request.user, "profile", None):
        if request.user.profile.role == Profile.Role.SEEKER:
            scored = rank_postings_for(request.user.profile.skill_set(), postings)
            ranked = [(posting, round(score * 100)) for posting, score in scored]

    return render(request, "jobsboard/posting_list.html", {"postings": postings, "ranked": ranked})


@login_required
def posting_create(request):
    if request.method == "POST":
        form = JobPostingForm(request.POST)
        if form.is_valid():
            posting = form.save(commit=False)
            posting.employer = request.user
            posting.save()  # triggers the notification signal
            return redirect("posting_list")
    else:
        form = JobPostingForm()
    return render(request, "jobsboard/posting_form.html", {"form": form})


@login_required
def posting_detail(request, pk):
    posting = get_object_or_404(JobPosting, pk=pk)
    score = None
    if getattr(request.user, "profile", None) and request.user.profile.role == Profile.Role.SEEKER:
        from .matching import match_score
        score = round(match_score(request.user.profile.skill_set(), posting.skill_set()) * 100)
    return render(request, "jobsboard/posting_detail.html", {"posting": posting, "score": score})


@login_required
def notifications(request):
    items = request.user.notifications.all()
    items.filter(is_read=False).update(is_read=True)
    return render(request, "jobsboard/notifications.html", {"notifications": items})
