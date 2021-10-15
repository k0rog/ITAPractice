from .utils.twitter_connector import TwitterWrapper
from django.views.generic import ListView, DetailView
from users.models import CustomUser
from .models import Game, Platform, Genre
from django.shortcuts import get_object_or_404
from django.db.models import Exists, OuterRef
from django.http import Http404


class GamesListView(ListView):
    context_object_name = 'games'
    template_name = 'gamehub/index.html'

    def get_queryset(self):
        # Limited for a while
        lower_rating = float(self.request.GET.get('lower_rating', '0'))
        upper_rating = float(self.request.GET.get('upper_rating', '10'))
        genres = self.request.GET.get('genres', ','.join([genre.name for genre in Genre.objects.all()])).split(',')
        platforms = self.request.GET.get('platforms', ','.join([platform.name for platform in Platform.objects.all()])).split(',')

        games = Game.objects.filter(rating__gte=lower_rating, rating__lte=upper_rating,
                                    genres__name__in=genres,
                                    platforms__name__in=platforms).annotate(
            in_musts=Exists(CustomUser.objects.filter(pk=self.request.user.id, musts__igdb_id=OuterRef('igdb_id')))
        ).distinct()

        return games

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data()

        games_count = len(context_data['games'])
        last_page = games_count // 30
        if games_count % 30 != 0:
            last_page += 1

        page = int(self.request.GET.get('page', 1))
        if page == 0:
            context_data['games'] = []
        elif page < 0:
            raise Http404("Page not found")
        else:
            context_data['games'] = context_data['games'][0+(page-1)*30:page*30]

        context_data['last_page'] = last_page
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
