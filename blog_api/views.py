from django.contrib.auth.models import User
from rest_framework import permissions as rest_permissions
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from . import serializers, permissions
from blog_api.models import Profile, Note


class AccountAPIView(ListAPIView):
    """ Представление для просмотра профилей """
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = serializers.AccountSerializer


class CreateUserView(CreateAPIView):
    """ Представление для регистрации пользователя """
    model = User
    permission_classes = [
        rest_permissions.AllowAny   # чтобы любой новый пользователь смог зарегистрироваться
    ]
    serializer_class = serializers.UserSignUpSerializer


class NoteAPIView(ListCreateAPIView):
    """ Создание и просмотр постов """
    permission_classes = [IsAuthenticated]
    queryset = Note.objects.all().order_by('-create_at')
    serializer_class = serializers.NoteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NoteDetailAPIView(RetrieveUpdateDestroyAPIView):
    """ Редактирование и удаление поста """
    permission_classes = [IsAuthenticated, permissions.OnlyAuthorEditNote]
    queryset = Note.objects.all()
    serializer_class = serializers.NoteSerializer
