from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.forms import ModelForm

from .models import (
    Task,
    UserProfile
)


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user_name', 'bio', 'profile_picture')

    # Add the following to the form to handle file uploads
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['profile_picture'].widget.attrs.update({'accept': 'image/*'})