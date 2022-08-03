from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import serializers

from blog_api.models import Profile, Note


class AccountUsernameSerializer(serializers.ModelSerializer):
    """ Сериализация данных для списка пользователей """
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Profile
        fields = ['user']


class NoteSerializer(serializers.ModelSerializer):
    """ Сериализация данных для постов """
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Note
        fields = (
            'id', 'title', 'note', 'create_at',
            'user',
        )

    def to_representation(self, instance):
        """ Переопределение вывода. Меняем формат даты в ответе """
        ret = super().to_representation(instance)
        # Конвертируем строку в дату по формату
        create_at = datetime.strptime(ret['create_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        # Конвертируем дату в строку в новом формате
        ret['create_at'] = create_at.strftime('%d %B %Y - %H:%M:%S')
        return ret


class AccountSerializer(serializers.ModelSerializer):
    """ Сериализация данных для списка пользователей """
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    follows = AccountUsernameSerializer(many=True, read_only=True)
    follow_count = serializers.SerializerMethodField()
    # notes_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'user', 'follow_count',
            # 'notes_count',
            'follows',
            # 'note',
        ]

    def get_follow_count(self, obj):
        return obj.follows.count()

    # def get_notes_count(self, obj):
    #     pass


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
