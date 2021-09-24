from rest_framework import viewsets
from gamehub.models import Game
from .serializers import GameListSerializer, GameDetailSerializer


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Game.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return GameListSerializer
        elif self.action == "retrieve":
            return GameDetailSerializer
