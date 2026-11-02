from django.urls import path

from . import views

urlpatterns = [
    path("", views.posting_list, name="posting_list"),
    path("new/", views.posting_create, name="posting_create"),
    path("<int:pk>/", views.posting_detail, name="posting_detail"),
    path("notifications/", views.notifications, name="notifications"),
]
