from django.forms import ModelForm
from .models import CustomUser
from django import forms


class UserRegistrationForm(ModelForm):
    # Why is it not given the default date type? Weird
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Repeat password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']

        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('User with this login already exists!')

        return username

    def clean_password(self):
        password = self.cleaned_data['password']

        if len(password) < 6:
            raise forms.ValidationError('Password is too short!')

        return password

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if password != password2:
            raise forms.ValidationError('Passwords are not the same')

        return password2

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']
        help_texts = {
            'username': None,
        }
