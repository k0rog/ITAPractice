from rest_framework import serializers
from gamehub.models import Game
from users.models import CustomUser


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'age', 'username', 'email',)


class UserMustSerializer(serializers.ModelSerializer):
    users_added = serializers.IntegerField()

    class Meta:
        model = Game
        fields = ('id', 'igdb_id', 'name', 'slug', 'cover', 'users_added')
