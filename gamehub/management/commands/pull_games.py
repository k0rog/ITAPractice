from django.core.management.base import BaseCommand
from gamehub.utils.igdb_connector import IGDBWrapper
from gamehub.models import Game, Platform, Genre, Screenshot
from datetime import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('-------------------------------------------------')
        print('-------------------------------------------------')
        print('-------------------------------------------------')
        print('-------------------------------------------------')
        print('-------------------------------------------------')
        igdb_api = IGDBWrapper()

        print('Collecting games start')
        total_start = datetime.now()
        games = igdb_api.get_game_list()[:5]
        print(f'Game list received in {datetime.now()-total_start}')

        print('Database pushing start')
        games_pushing = datetime.now()
        for i, game in enumerate(games):
            start = datetime.now()
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
            print(f'    Game {i} pushed in {datetime.now() - start}')
        print(f'Games pushed in {datetime.now() - games_pushing}')
        print(f'Collecting games ended in {datetime.now() - total_start}')
