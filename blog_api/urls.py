from django.urls import path, include

from . import views

urlpatterns = [
    path('accounts/profile/', views.AccountAPIView.as_view())
]
