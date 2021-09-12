from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, UserAuthorizationForm
from .utils.functions import get_age_from_birth_date
from django.core.mail import send_mail


class SignUpView(CreateView):
    template_name = 'users/registration.html'
    success_url = reverse_lazy('authorization')
    form_class = UserRegistrationForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(form.cleaned_data['password'])
        self.object.age = get_age_from_birth_date(form.cleaned_data['birth_date'])
        self.object.save()

        # Should I do this in the other place?
        send_mail(subject='Registration',
                  message='You successfully registered at GameHub',
                  from_email=None,
                  recipient_list=[form.cleaned_data['email']],
                  fail_silently=True)

        return super().form_valid(form)


class SignInView(LoginView):
    template_name = 'users/authorization.html'
    authentication_form = UserAuthorizationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
        return redirect('games')


class UserProfileView(TemplateView):
    template_name = 'users/user_profile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            return handler(request, *args, **kwargs)
        else:
            return redirect('login')

    def get(self, request, *args, **kwargs):
        user = request.user
        return self.render_to_response({'user': user})
