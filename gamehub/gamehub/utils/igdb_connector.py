import requests
from datetime import datetime, timedelta
from django.conf import settings


class IGDBWrapper:
    _last_token_request = None
    _expires_in = None
    _current_token = None
    ROOT_ENDPOINT = 'https://api.igdb.com/v4/'

    def __init__(self):
        self.__headers = {
            'Client-ID': settings.IGDB_CLIENT_ID,
            'Authorization': f'Bearer {self._get_token()}'
        }

    def get_game_list(self, params):
        return self.get_data_from_endpoint('games', params=params)

    def get_game(self, game_name, params):
        # The value of the search parameter must be wrapped by ""
        params['search'] = f'"{game_name.replace("-", " ")}"'

        response = self.get_data_from_endpoint('games', params=params)

        # Returns games by degree of collision.
        # If not found, we will raise 404. If found - return the most probable
        if len(response) == 0:
            return None
        game = response[0]

        # Put the data in order
        game['first_release_date'] = datetime.fromtimestamp(game['first_release_date']).strftime('%B %d, %Y')
        if 'rating' in game:
            game['rating'] = round(game['rating'] / 10, 1)
        if 'aggregated_rating' in game:
            game['aggregated_rating'] = round(game['aggregated_rating'] / 10, 1)

        return game

    def get_screenshots(self, game_id):
        params = {
                'fields': 'url',
                'where': f"game = {game_id}",
                'limit': 6,
                'sort': 'popularity desc'
            }
        return self.get_data_from_endpoint('screenshots', params=params)

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
