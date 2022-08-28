from django.urls import path

from . import views

urlpatterns = [
    # path('accounts/profile/', views.AccountAPIView.as_view()),
    path('accounts/profiles/', views.AccountsAPIView.as_view()),
    path('accounts/profiles/<int:pk>/', views.AccountDetailAPIView.as_view()),
    path('accounts/profiles/<int:pk>/follows/', views.AccountFollowsAPIView.as_view()),
    path('accounts/signup/', views.CreateUserView.as_view()),
    path('notes/', views.NoteAPIView.as_view()),
    path('notes/<int:pk>/', views.NoteDetailAPIView.as_view()),
    path('feed/', views.FeedAPIView.as_view()),
    path('feed/<int:pk>/', views.NoteDetailAPIView.as_view())
]
