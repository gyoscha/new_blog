from django.db.models import Count
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions as rest_permissions
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, \
    RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
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

        return queryset\
            .filter(user__username__in=follows)\
            .order_by('-create_at') \
            .select_related('user') \
            .prefetch_related('read_posts',)
            # .exclude(read_posts=user.profile)   # можно исключить прочитанные посты из ленты, но тогда отваливаются фильтры


class AccountsAPIView(ListAPIView):
    """ Представление для просмотра профилей """
    permission_classes = [IsAuthenticated]
    # сортировка по количеству постов в порядке убывания
    queryset = Profile.objects.all().annotate(cnt=Count('user__note')).order_by('-cnt')
    serializer_class = serializers.AccountSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.select_related('user').prefetch_related('user__note', 'follows')


class AccountDetailAPIView(RetrieveUpdateAPIView):
    """ Представление для просмотра отдельного профиля """
    permission_classes = [IsAuthenticated, permissions.OnlyAuthor]
    queryset = Profile.objects.all()
    serializer_class = serializers.AccountDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset \
            .select_related('user')\
            .prefetch_related('user__note', 'follows')


# class AccountAPIView(ListAPIView):
#     """ Представление для просмотра своего профиля """
#     permission_classes = [IsAuthenticated]
#     queryset = Profile.objects.all()
#     serializer_class = serializers.AccountDetailSerializer
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         current_user = self.request.user
#
#         return queryset.filter(user=current_user) \
#             .select_related('user') \
#             .prefetch_related('user__note', 'follows')


class AccountFollowsAPIView(RetrieveAPIView):
    """ Представление для просмотра подписок пользователя """
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = serializers.AccountFollowsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset \
            .select_related('user') \
            .prefetch_related('follows__user')


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

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset \
            .select_related('user')\
            .prefetch_related('read_posts')


class NoteDetailAPIView(RetrieveUpdateDestroyAPIView):
    """ Редактирование и удаление поста """
    permission_classes = [IsAuthenticated, permissions.OnlyAuthor]
    queryset = Note.objects.all()
    serializer_class = serializers.NoteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset \
            .select_related('user')

    def get_object(self):
        """ При открытии поста он автоматически становится прочитанным пользователем """
        obj = super().get_object()
        user = self.request.user
        obj.read_posts.add(user.profile)
        return obj
