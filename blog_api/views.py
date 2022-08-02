from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from . import serializers
from blog_api.models import Profile


class AccountAPIView(ListAPIView):
    """ Представление для просмотра профилей """
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = serializers.AccountSerializer


class CreateUserView(CreateAPIView):
    """ Представление для регистрации пользователя """
    model = User
    permission_classes = [
        permissions.AllowAny   # чтобы любой новый пользователь смог зарегистрироваться
    ]
    serializer_class = serializers.UserSignUpSerializer
