from django.contrib.auth.models import User
from rest_framework import serializers

from blog_api.models import Profile


class AccountSerializer(serializers.ModelSerializer):
    """ Сериализация данных для списка пользователей """
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Profile
        fields = (
            'user', 'follows'
        )


class UserSignUpSerializer(serializers.ModelSerializer):
    """ Сериализация данных для регистрации пользователя """
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = User(**validated_data)
        # Хэшируем пароль
        user.set_password(validated_data['password'])
        user.save()
        return user
