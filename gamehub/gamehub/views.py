from .utils import igdb_connector, twitter_connector
from django.views.generic import ListView, DetailView
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
            'fields': 'name, genres.name, cover.url, slug',
            'limit': 6,
            'where': 'cover != null'
        }
        games = igdb_connector.get_game_list(params)

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

    # Тут вводим поисковой запрос к twitter api.

    # Честно, без понятия, как сделать правильный поиск. Потому что некоторые игры называются
    # слишком сложно и по хэштегу не поищешь (например, "THE LEGEND OF ZELDA: BREATH OF THE WILD - THE MASTER TRIALS").
    # По упоминанию в твите тоже не ищет. Можно было бы выделить ключевые слова и искать по упоминанию их,
    # я даже нашёл алгоритмы, но текст слишком маленький, да и работать это вряд ли будет.
    # Ну я, собственно, сделал просто по упоминанию в твите названия игры и забил, так как не уверен, что
    # смогу что-то придумать быстро. Но если тут это от меня требуется - скажи, я придумаю
    # Но предупреждаю, что твиты с упоминанием некоторых игр могут содержать ругательства :(

        game_name = (context_data['object']['name'])
        query = f'"{game_name}" lang:en'
        context_data['tweets'] = twitter_connector.get_tweets(query)

        return context_data
