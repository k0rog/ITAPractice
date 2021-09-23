import requests
import time
from datetime import datetime, timedelta
from django.conf import settings


class IGDBWrapper:
    _last_token_request = None
    _expires_in = None
    _current_token = None
    ROOT_ENDPOINT = 'https://api.igdb.com/v4/'
    OLDEST_GAME_RELEASE_DATE = round(time.mktime(datetime(year=2020, month=1, day=1).timetuple()))
    GAME_FIELDS = ['name', 'genres.name', 'cover.url', 'slug', 'genres.name', 'platforms.abbreviation', 'summary',
                   'first_release_date', 'rating', 'rating_count',
                   'aggregated_rating', 'aggregated_rating_count', 'screenshots.url']

    def __init__(self):
        self.__headers = {
            'Client-ID': settings.IGDB_CLIENT_ID,
            'Authorization': f'Bearer {self._get_token()}'
        }

    def get_game_list(self):
        params = {
            'fields': ', '.join(IGDBWrapper.GAME_FIELDS),
            # Without specifying a limit, it returns 10 games despite filtering
            # 'limit': 5,
            'limit': self.get_games_count(),
            'where': f"first_release_date > {IGDBWrapper.OLDEST_GAME_RELEASE_DATE} & "
                     f"{' & '.join([field + '!=null' for field in IGDBWrapper.GAME_FIELDS])}"
        }
        raw_games = self.get_data_from_endpoint('games', params)

        games = []
        for raw_game in raw_games:
            raw_game['first_release_date'] = datetime.fromtimestamp(raw_game['first_release_date']).date()
            raw_game['rating'] = round(raw_game['rating'] / 10, 1)
            raw_game['aggregated_rating'] = round(raw_game['aggregated_rating'] / 10, 1)
            raw_game['cover'] = raw_game['cover']['url']

            game = {
                'id': raw_game['id'],
                'genres': raw_game['genres'],
                'platforms': raw_game['platforms'],
                'screenshots': raw_game['screenshots'],
            }

            game['defaults'] = {k: v for k, v in raw_game.items() if k not in game.keys()}

            games.append(game)

        return games

    def get_games_count(self):
        params = {
            'where': f"first_release_date > {IGDBWrapper.OLDEST_GAME_RELEASE_DATE} & "
                     f"{' & '.join([field+'!=null' for field in IGDBWrapper.GAME_FIELDS])}"
        }
        return self.get_data_from_endpoint('games/count', params=params)['count']

    def get_data_from_endpoint(self, endpoint, params):
        # Converting a dictionary to a string of the desired format for a query
        data = '; '.join([f'{key} {value}' for key, value in params.items()]) + ';'

        return requests.post(IGDBWrapper.ROOT_ENDPOINT + endpoint,
                             headers=self.__headers,
                             data=data).json()

    @staticmethod
    def _get_token():
        # The token is issued for almost 2 months (on average). We will not ask him every time
        # Saves a second
        if not IGDBWrapper._current_token or not IGDBWrapper._last_token_request or \
                IGDBWrapper._last_token_request + timedelta(seconds=IGDBWrapper._expires_in) < datetime.now():
            params = {
                'client_id': f'{settings.IGDB_CLIENT_ID}',
                'client_secret': f'{settings.IGDB_CLIENT_SECRET}',
                'grant_type': 'client_credentials',
            }
            IGDBWrapper._last_token_request = datetime.now()
            IGDBWrapper._current_token, IGDBWrapper._expires_in, _ = requests.post(f'https://id.twitch.tv/oauth2/token',
                                                                                   params=params).json().values()
        return IGDBWrapper._current_token
