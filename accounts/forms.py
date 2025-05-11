# accounts / forms.py
from django import forms
from .models import CustomUser


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'gender', 'position', 'department', 'profile_picture']

    profile_picture = forms.ImageField(required=False)
