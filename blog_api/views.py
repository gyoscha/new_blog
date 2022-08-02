from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from . import serializers
from blog_api.models import Profile


class AccountAPIView(ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = serializers.AccountSerializer
