from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, UserAuthorizationForm
from .utils.functions import get_age_from_birth_date
from django.core.mail import send_mail
from gamehub.utils.igdb_connector import IGDBWrapper
from gamehub.models import Game
from .models import CustomUser
from .utils.mixins import AuthenticatedMixin
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseNotAllowed


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

        igdb_api = IGDBWrapper()

        games = []
        for must_game in user.musts.all():
            users_added = CustomUser.objects.filter(musts__igdb_id=must_game.igdb_id).count()
            game = igdb_api.get_game_by_id(must_game.igdb_id)
            game['users_added'] = users_added
            games.append(game)

        return games


# Didn't find a suitable class
def musts(request):
    if not request.user or not request.user.is_authenticated:
        return HttpResponseForbidden()

    if request.method not in ['POST', 'DELETE']:
        return HttpResponseNotAllowed(['POST', 'DELETE'])

    body = request.body.decode(request.encoding)
    igdb_id = int(body.split('=')[-1])

    # temporary. It's obvious, games will always exist when I will pull them from IGDB to database
    try:
        game = Game.objects.get(igdb_id=igdb_id)
    except Game.DoesNotExist:
        game = Game.objects.create(igdb_id=igdb_id)

    user = CustomUser.objects.get(pk=request.user.id)

    if request.method == 'DELETE':
        user.musts.remove(game)
    elif request.method == 'POST':
        user.musts.add(game)

    return HttpResponse(status=200)




