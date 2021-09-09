from django.forms import ModelForm
from .models import CustomUser
from django import forms
from django.forms import DateInput


class UserRegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    re_password = forms.CharField(widget=forms.PasswordInput, label='Repeat password')
    # Why is it not given the default date type? Weird
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'birthday', 'password', 're_password']
        help_texts = {
            'username': None,
        }
