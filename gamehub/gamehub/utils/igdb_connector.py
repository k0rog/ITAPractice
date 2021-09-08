import os
import requests
from datetime import datetime, timedelta
# Ну я в курсе, что, скорее всего, это нужно было в класс оборачивать
# Но я не был уверен, что на каждый запрос стоит создавать экземпляр этого класса
# Поэтому сделал вот таким модулем. Если это не правильно - нет проблем, переделаю
# подозреваю, что тут должен быть синглтон


def get_game_list(params):
    return get_data_from_endpoint('https://api.igdb.com/v4/games/', params=params)


def get_game(game_name, params):
    # Значение параметра search нужно обязательно оборачивать в ""
    params['search'] = f'"{game_name.replace("-", " ")}"'

    response = get_data_from_endpoint('https://api.igdb.com/v4/games/', params=params)

    # Возвращает игры по степени сопадения. Если не нашло - поднимем 404, а если нашло - вернём самую вероятную
    if len(response) == 0:
        return None
    game = response[0]
    # Привожу данные в порядок
    game['first_release_date'] = datetime.fromtimestamp(game['first_release_date']).strftime('%B %d, %Y')
    if 'rating' in game:
        game['rating'] = round(game['rating'] / 10, 1)
    if 'aggregated_rating' in game:
        game['aggregated_rating'] = round(game['aggregated_rating'] / 10, 1)

    return game


def get_data_from_endpoint(endpoint, params):
    # Преобразование словаря в строку нужного формата для запроса
    data = '; '.join([f'{key} {value}' for key, value in params.items()]) + ';'

    return requests.post(endpoint,
                         headers=_get_headers(),
                         data=data).json()


def _get_token(client_id, client_secret):
    params = {
        'client_id': f'{client_id}',
        'client_secret': f'{client_secret}',
        'grant_type': 'client_credentials',
    }

    access_token, expires_in, _ = requests.post(f'https://id.twitch.tv/oauth2/token',
                                                params=params).json().values()

    return access_token, expires_in


def _get_headers():
    # Токен выдаётся почти на 2 месяца (в среднем). Не будем его запрашивать каждый раз
    # Экономит секунду
    global _current_token, _last_token_request, _expires_in

    if not _current_token or not _last_token_request or \
            _last_token_request + timedelta(seconds=_expires_in) < datetime.now():

        _last_token_request = datetime.now()
        _current_token, _expires_in = _get_token(os.environ.get('Client_id'),
                                                 os.environ.get('Client_secret'))

    return {
        'Client-ID': os.environ.get('Client_id'),
        'Authorization': f'Bearer {_current_token}'
    }


_last_token_request = None
_expires_in = None
_current_token = None
