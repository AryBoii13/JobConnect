from django.urls import path

from . import views

urlpatterns = [
    path("upload/", views.upload_resume, name="upload_resume"),
    path("<int:pk>/", views.resume_detail, name="resume_detail"),
]
