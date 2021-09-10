from datetime import date
from django.shortcuts import render
from .forms import UserRegistrationForm, UserAuthorizationForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from .models import CustomUser


def register_user(request):
    if request.method == 'GET':
        form = UserRegistrationForm(request.POST or None)
        return render(request, 'users/registration.html', {'form': form})
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.birthday = form.cleaned_data['birthday']
            user.save()
            return redirect('authorization')
        return render(request, 'users/registration.html', {'form': form})


def authorize_user(request):
    if request.method == 'GET':
        form = UserAuthorizationForm(request.POST or None)
        return render(request, 'users/authorization.html', {'form': form})
    elif request.method == 'POST':
        form = UserAuthorizationForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            return redirect('games')
        return render(request, 'users/authorization.html', {'form': form})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('games')
    return redirect(request.build_absolute_uri())


def profile_page(request):
    if not request.user or not request.user.is_authenticated:
        raise Http404('')
    user = request.user

    today = date.today()
    born = user.birthday

    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    data = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'age': age
    }

    return render(request, 'users/user_profile.html', data)
