from .utils.twitter_connector import TwitterWrapper
from django.views.generic import ListView, DetailView
from users.models import CustomUser
from .models import Game, Platform, Genre
from django.shortcuts import get_object_or_404
from django.db.models import Exists, OuterRef


class GamesListView(ListView):
    context_object_name = 'games'
    template_name = 'gamehub/index.html'

    def get_queryset(self):
        # Limited for a while
        games = Game.objects.all().annotate(
            in_musts=Exists(CustomUser.objects.filter(pk=self.request.user.id, musts__igdb_id=OuterRef('igdb_id')))
        )[:10]

        return games

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data()

        context_data['platforms'] = Platform.objects.all()
        context_data['genres'] = Genre.objects.all()

        return context_data


class GameDetailView(DetailView):
    template_name = 'gamehub/detail_page.html'
    context_object_name = 'game'

    def get_object(self, queryset=None):
        game = get_object_or_404(Game, slug=self.kwargs['slug'])
        game.in_musts = CustomUser.objects.filter(pk=self.request.user.id, musts__igdb_id=game.igdb_id).exists()

        return game

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()

        game_name = context_data['object'].name

        twitter_api = TwitterWrapper()
        # Search query to twitter api.
        query = f'"{game_name}" lang:en'
        context_data['tweets'] = twitter_api.get_tweets(query)

        return context_data
