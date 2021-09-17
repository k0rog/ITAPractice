from .utils.igdb_connector import IGDBWrapper
from .utils.twitter_connector import TwitterWrapper
from django.views.generic import ListView, DetailView
from django.http import Http404
from users.models import CustomUser


class GamesListView(ListView):
    context_object_name = 'games'
    template_name = 'gamehub/index.html'

    def get_queryset(self):
        params = {
            'fields': 'name, genres.name, cover.url, slug',
            'limit': 6,
            'where': 'cover != null'
        }

        igdb_api = IGDBWrapper()
        games = igdb_api.get_game_list(params)

        if self.request.user and self.request.user.is_authenticated:
            for game in games:
                if CustomUser.objects.filter(pk=self.request.user.id, musts__igdb_id=game['id']).exists():
                    game['in_musts'] = True
                else:
                    game['in_musts'] = False

        return games


class GameDetailView(DetailView):
    template_name = 'gamehub/detail_page.html'
    context_object_name = 'game'

    def get_object(self, queryset=None):
        params = {
            'fields': 'name, genres.name, platforms.abbreviation, summary,'
                      'first_release_date, rating, rating_count,'
                      'aggregated_rating, aggregated_rating_count'
        }
        igdb_api = IGDBWrapper()
        game = igdb_api.get_game(self.kwargs['slug'],
                                 params=params)
        if not game:
            raise Http404('Game not found')

        if self.request.user and self.request.user.is_authenticated:
            if CustomUser.objects.filter(pk=self.request.user.id, musts__igdb_id=game['id']).exists():
                game['in_musts'] = True
            else:
                game['in_musts'] = False

        return game

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()

        igdb_api = IGDBWrapper()
        context_data['screenshots'] = igdb_api.get_screenshots(int(context_data['object']['id']))

        game_name = context_data['object']['name']

        twitter_api = TwitterWrapper()
        # Search query to twitter api.
        query = f'"{game_name}" lang:en'
        context_data['tweets'] = twitter_api.get_tweets(query)

        return context_data
