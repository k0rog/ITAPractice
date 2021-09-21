from django.views import View
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, UserAuthorizationForm
from .utils.functions import get_age_from_birth_date
from django.core.mail import send_mail
from gamehub.models import Game
from .models import CustomUser
from .utils.mixins import AuthenticatedMixin
from django.http import HttpResponse
from django.db.models import Count


class SignUpView(CreateView):
    template_name = 'users/registration.html'
    success_url = reverse_lazy('authorization')
    form_class = UserRegistrationForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(form.cleaned_data['password'])
        self.object.age = get_age_from_birth_date(form.cleaned_data['birth_date'])
        self.object.save()

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


class UserProfileView(AuthenticatedMixin, TemplateView):
    template_name = 'users/user_profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        return self.render_to_response({'user': user})


class UserMustsView(ListView):
    context_object_name = 'games'
    template_name = 'users/musts.html'

    def get_queryset(self):
        user = self.request.user

        games = Game.objects.filter(customuser=user).annotate(users_added=Count('customuser'))

        return games


class MustsView(AuthenticatedMixin, View):
    http_method_names = ['post', 'delete']

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        body = request.body.decode(request.encoding)
        igdb_id = int(body.split('=')[-1])

        game = Game.objects.get(igdb_id=igdb_id)
        user = CustomUser.objects.get(pk=request.user.id)

        self.game = game
        self.user = user

    def delete(self, *args, **kwargs):
        self.user.musts.remove(self.game)
        return HttpResponse(status=200)

    def post(self, *args, **kwargs):
        self.user.musts.add(self.game)
        return HttpResponse(status=200)
