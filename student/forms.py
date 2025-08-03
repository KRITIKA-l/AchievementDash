from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomSignupForm(UserCreationForm):
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    location = forms.CharField(required=False, max_length=100)
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'date_of_birth', 'location', 'bio']
