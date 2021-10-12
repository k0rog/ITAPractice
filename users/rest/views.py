from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets, response
from gamehub.models import Game
from users.models import CustomUser
from .serializers import UserDetailSerializer, UserMustSerializer


class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer


class MustsViewSet(viewsets.ModelViewSet):
    serializer_class = UserMustSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Game.objects.filter(customuser=self.request.user).annotate(users_added=Count('customuser'))

    def destroy(self, request, *args, **kwargs):
        game = get_object_or_404(Game, pk=kwargs['game_id'])
        CustomUser.objects.get(pk=kwargs['pk']).musts.remove(game)

        return response.Response(status=200)

    def create(self, request, *args, **kwargs):
        game = get_object_or_404(Game, pk=kwargs['game_id'])
        CustomUser.objects.get(pk=kwargs['pk']).musts.add(game)

        return response.Response(status=200)
