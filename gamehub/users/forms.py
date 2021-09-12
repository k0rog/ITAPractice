from .models import CustomUser
from django import forms
from .utils.functions import get_age_from_birth_date


class UserRegistrationForm(forms.ModelForm):
    # Why is it not given the default date type? Weird
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Repeat password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        age = get_age_from_birth_date(birth_date)
        if age < 12:
            raise forms.ValidationError('You are too small to register!')
        return birth_date

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


class UserAuthorizationForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Username {username} not found')

        user = CustomUser.objects.filter(username=username).first()
        if user and not user.check_password(password):
            raise forms.ValidationError('Wrong password')

        return self.cleaned_data

    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        help_texts = {
            'username': None,
        }
        widgets = {
            'password': forms.PasswordInput
        }
