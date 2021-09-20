from django.core.management.base import BaseCommand
from gamehub.utils.igdb_connector import IGDBWrapper


class PullGames(BaseCommand):
    def handle(self, *args, **options):
        igdb_api = IGDBWrapper()

        games = igdb_api.get_game_list()
