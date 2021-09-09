from django.shortcuts import render
from .forms import UserRegistrationForm


def registration(request):
    if request.method == 'GET':
        form = UserRegistrationForm()
        print('--------------------')
        print(form)
        return render(request, 'users/registration.html', {'form': form})
    return None


def authorization(request):
    return render(request, '')
