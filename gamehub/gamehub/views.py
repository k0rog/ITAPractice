from .utils import igdb_connector, twitter_connector
from django.views.generic import ListView, DetailView
import re
from django.http import Http404


class GamesListView(ListView):
    context_object_name = 'games'
    template_name = 'gamehub/index.html'

    def get_queryset(self):
        # Изначально я совершил ошибку и отправлял запрос, передавая фильтры в params
        # Потом нашёл, что нужно передавать в data, но тогда все фильтры нужно будет писать
        # В одной строке, что как-то не очень красиво и интуитивно.
        # Поэтому я задаю фильтры в словаре, а потом паршу его в igdb_connector'e.
        # Возможно, это не правильно и нужно исправлять, жду фидбек)
        params = {
            'fields': 'name, genres.name, cover.url',
            'limit': 6,
            'where': 'cover != null'
        }
        games = igdb_connector.get_game_list(params)

        reg = re.compile('[^a-zA-Z ]')
        for game in games:
            game['slug'] = reg.sub('', game['name']).lower().replace(' ', '-')
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
        game = igdb_connector.get_game(self.kwargs['slug'],
                                       params=params)
        if not game:
            raise Http404('Game not found')

        return game

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data['screenshots'] = igdb_connector.get_data_from_endpoint(
            endpoint='https://api.igdb.com/v4/screenshots',
            params={
                'fields': 'url',
                'where': f"game = {context_data['object']['id']}",
                'limit': 6,
                'sort': 'popularity desc'
            },
        )
        # Имеет хэштег с названием игры И(логическое) английский язык твита
        # search_query = context_data['object']['name']
        # context_data['tweets'] = twitter_connector.get_tweets(f"\"{search_query}\" lang:en")

        reg = re.compile('[^a-zA-Z ]')
        search_query = reg.sub('', context_data['object']['name']).replace('  ', '')
        print(search_query.replace([' ', '  '], '').split(' '))
        search_query = " OR ".join(search_query.split(' '))
        context_data['tweets'] = twitter_connector.get_tweets(f"({search_query}) lang:en")

        return context_data
