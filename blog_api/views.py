from django.db.models import Count
from django.contrib.auth.models import User
from rest_framework import permissions as rest_permissions
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, \
    RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from . import serializers, permissions
from blog_api.models import Profile, Note

# Todo Изменить профили все с подсчетом постов и профиль только свой после успешного входа


class FeedAPIView(ListAPIView):
    """ Представление для просмотра ленты постов из подписок """
    permission_classes = [IsAuthenticated]
    queryset = Note.objects.all()
    serializer_class = serializers.NoteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        follows = [i for i in user.profile.follows.all()]

        return queryset.filter(user__username__in=follows).order_by('-create_at')


class AccountAPIView(ListAPIView):
    """ Представление для просмотра профилей """
    permission_classes = [IsAuthenticated]
    # сортировка по количеству постов в порядке убывания
    queryset = Profile.objects.all().annotate(cnt=Count('user__note')).order_by('-cnt')
    serializer_class = serializers.AccountSerializer


class AccountDetailAPIView(RetrieveUpdateAPIView):
    """ Представление для просмотра отдельного профиля """
    permission_classes = [IsAuthenticated, permissions.OnlyAuthor]
    queryset = Profile.objects.all()
    serializer_class = serializers.AccountDetailSerializer


class AccountFollowsAPIView(RetrieveAPIView):
    """ Представление для просмотра подписок пользователя """
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = serializers.AccountFollowsSerializer


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
    permission_classes = [IsAuthenticated, permissions.OnlyAuthor]
    queryset = Note.objects.all()
    serializer_class = serializers.NoteSerializer
