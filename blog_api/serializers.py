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
