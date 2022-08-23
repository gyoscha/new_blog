from django.db.models import Count
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions as rest_permissions
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, \
    RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from . import serializers, permissions
from blog_api.models import Profile, Note


class FeedAPIView(ListAPIView):
    """ Представление для просмотра ленты постов из подписок """
    permission_classes = [IsAuthenticated]
    queryset = Note.objects.all()
    serializer_class = serializers.NoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['read_posts']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        follows = [i for i in user.profile.follows.all()]

        return queryset.filter(user__username__in=follows).order_by('-create_at')
            # .exclude(read_posts=user.profile)   # можно исключить прочитанные посты из ленты, но тогда отваливаются фильтры


class FeedDetailAPIView(RetrieveAPIView):
    """ Представление для детального просмотра поста из ленты """
    permission_classes = [IsAuthenticated]
    queryset = Note.objects.all()
    serializer_class = serializers.NoteDetailSerializer

    def get_object(self):
        """ При открытии поста он автоматически становится прочитанным пользователем """
        obj = super().get_object()
        user = self.request.user
        obj.read_posts.add(user.profile)
        return obj


class AccountsAPIView(ListAPIView):
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


# class AccountAPIView(RetrieveUpdateAPIView):
#     """ Представление для просмотра своего профиля """
#     permission_classes = [IsAuthenticated]
#     queryset = Profile.objects.all()
#     serializer_class = serializers.AccountDetailSerializer
#     lookup_field = 'user_id'
#
#     def get_queryset(self):
#         current_user = self.request.user
#
#         return Profile.objects.get(user_id=current_user)


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
    serializer_class = serializers.NoteDetailSerializer

    def get_object(self):
        """ При открытии поста он автоматически становится прочитанным пользователем """
        obj = super().get_object()
        user = self.request.user
        obj.read_posts.add(user.profile)
        return obj
