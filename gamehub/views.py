from .utils.twitter_connector import TwitterWrapper
from django.views.generic import ListView, DetailView
from users.models import CustomUser
from .models import Game
from django.shortcuts import get_object_or_404


class GamesListView(ListView):
    context_object_name = 'games'
    template_name = 'gamehub/index.html'

    def get_queryset(self):
        games = Game.objects.all()

        if self.request.user and self.request.user.is_authenticated:
            for game in games:
                game.in_musts = CustomUser.objects.filter(pk=self.request.user.id, musts__igdb_id=game.igdb_id).exists()

        return games


class GameDetailView(DetailView):
    template_name = 'gamehub/detail_page.html'
    context_object_name = 'game'

    def get_object(self, queryset=None):
        game = get_object_or_404(Game, slug=self.kwargs['slug'])

        if self.request.user and self.request.user.is_authenticated:
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
