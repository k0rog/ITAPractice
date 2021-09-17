import requests
from datetime import datetime
from django.conf import settings


class TwitterWrapper:
    def __init__(self):
        self.__headers = {
            'Authorization': f'Bearer {settings.TWITTER_BEARER_TOKEN}'
        }
        self.__params = {
            'tweet.fields': 'text,created_at',
            'user.fields': 'username',
            'expansions': 'author_id',
        }

    def get_tweets(self, query):
        self.__params['query'] = query

        response = requests.get("https://api.twitter.com/2/tweets/search/recent",
                                headers=self.__headers, params=self.__params).json()

        if response['meta']['result_count'] == 0:
            return {}

        tweets = response['data']
        users = response['includes']['users']

        # We combine dictionaries for only the first five tweets. By default, 10 pieces come, you can't get less
        # according to the endpoint documentation. And it makes no sense to send so many tweets to a page.
        for i, tweet in enumerate(tweets):
            for user in users:
                if user['id'] == tweet['author_id']:
                    tweet['author_username'] = user['username']
                    users.remove(user)
                break
            if i == 4:
                break
        tweets = tweets[:5]

        # Format the dictionary
        for tweet in tweets:
            tweet.pop('id', None)
            tweet.pop('author_id', None)
            date = datetime.strptime(tweet['created_at'][:-5], '%Y-%m-%dT%H:%M:%S').strftime('%B %d')
            tweet['created_at'] = date

        return tweets
