from django.core.management.base import BaseCommand
from gamehub.utils.igdb_connector import IGDBWrapper
from gamehub.models import Game, Platform, Genre, Screenshot


class Command(BaseCommand):
    def handle(self, *args, **options):
        igdb_api = IGDBWrapper()

        games = igdb_api.get_game_list()[:50]
        for i, game in enumerate(games):
            new_game, created = Game.objects.update_or_create(
                igdb_id=game['id'],
                defaults=game['defaults']
            )
            for screenshot in game['screenshots']:
                Screenshot.objects.get_or_create(url=screenshot['url'], game=new_game)

            for genre in game['genres']:
                genre, _ = Genre.objects.get_or_create(name=genre['name'])
                new_game.genres.add(genre)

            for platform in game['platforms']:
                try:
                    platform, _ = Platform.objects.get_or_create(name=platform['abbreviation'])
                except KeyError:
                    platform, _ = Platform.objects.get_or_create(name=platform['name'])
                new_game.platforms.add(platform)
