from rest_framework import serializers
from gamehub.models import Game


class GameListSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

    class Meta:
        model = Game
        fields = ('id', 'igdb_id', 'name', 'slug', 'cover', 'genres',)


class GameDetailSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    platforms = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

    class Meta:
        model = Game
        exclude = ('igdb_id',)
