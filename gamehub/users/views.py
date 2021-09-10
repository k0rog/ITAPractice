from django.shortcuts import render
from .forms import UserRegistrationForm
from django.shortcuts import redirect


def registration(request):
    if request.method == 'GET':
        form = UserRegistrationForm(request.POST or None)
        return render(request, 'users/registration.html', {'form': form})
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('games')
        return render(request, 'users/registration.html', {'form': form})


def authorization(request):
    return render(request, '')
