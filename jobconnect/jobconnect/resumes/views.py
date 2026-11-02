from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ResumeUploadForm
from .utils import extract_skills, extract_text


@login_required
def upload_resume(request):
    if request.method == "POST":
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()

            text = extract_text(resume.file)
            skills = extract_skills(text)
            resume.raw_text = text
            resume.extracted_skills = ", ".join(skills)
            resume.save()

            # Fold the extracted skills into the user's profile so the
            # matching logic in jobsboard can use them.
            profile = request.user.profile
            existing = profile.skill_set()
            profile.skills = ", ".join(sorted(existing | set(skills)))
            profile.save()

            return redirect("resume_detail", pk=resume.pk)
    else:
        form = ResumeUploadForm()
    return render(request, "resumes/upload.html", {"form": form})


@login_required
def resume_detail(request, pk):
    resume = request.user.resumes.get(pk=pk)
    return render(request, "resumes/detail.html", {"resume": resume})
