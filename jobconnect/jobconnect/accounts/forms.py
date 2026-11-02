from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=Profile.Role.choices)
    headline = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "role", "headline"]

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Profile.objects.create(
                user=user,
                role=self.cleaned_data["role"],
                headline=self.cleaned_data.get("headline", ""),
            )
        return user
