import os
import requests
from datetime import datetime


_headers = {
    'Authorization': f'Bearer {os.environ.get("Bearer_token")}'
}

_params = {
    'tweet.fields': 'text,created_at',
    'user.fields': 'username',
    'expansions': 'author_id',
}


def get_tweets(query):
    _params['query'] = query

    response = requests.get("https://api.twitter.com/2/tweets/search/recent",
                            headers=_headers, params=_params).json()

    if response['meta']['result_count'] == 0:
        return {}

    # Данные приходят в двух разных словарях!
    tweets = response['data']
    users = response['includes']['users']

    # Объединяем словари только для пяти первых твитов. По умолчанию приходит 10 штук, меньше нельзя
    # по документации ендпоинта. А отправлять столько твитов на страничку не имеет смысла
    # (zip не поможет, так как они не отсортированы)
    for i, tweet in enumerate(tweets):
        for user in users:
            if user['id'] == tweet['author_id']:
                tweet['author_username'] = user['username']
                users.remove(user)
            break
        if i == 4:
            break
    tweets = tweets[:5]

    # Ну и форматируем словарик
    for tweet in tweets:
        tweet.pop('id', None)
        tweet.pop('author_id', None)
        date = datetime.strptime(tweet['created_at'][:-5], '%Y-%m-%dT%H:%M:%S')
        date = date.strftime('%B %d')
        tweet['created_at'] = date

    return tweets

