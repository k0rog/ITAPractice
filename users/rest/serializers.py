from rest_framework import serializers
from gamehub.models import Game
from users.models import CustomUser
from djoser.serializers import UserCreateSerializer, ValidationError


class UserRegistrationSerializer(UserCreateSerializer):
    def validate_age(self, value):
        if value < 12:
            raise ValidationError('User is too small to register. Minimum age 12 years.')

        return value

    class Meta(UserCreateSerializer.Meta):
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'age')


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'age', 'username', 'email',)


class UserMustSerializer(serializers.ModelSerializer):
    users_added = serializers.IntegerField()

    class Meta:
        model = Game
        fields = ('id', 'igdb_id', 'name', 'slug', 'cover', 'users_added')
