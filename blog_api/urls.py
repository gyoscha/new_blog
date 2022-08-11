from django.urls import path

from . import views

urlpatterns = [
    # path('accounts/profile/', ),
    path('accounts/profiles/', views.AccountAPIView.as_view()),
    path('accounts/profiles/<int:pk>/', views.AccountDetailAPIView.as_view()),
    path('accounts/signup/', views.CreateUserView.as_view()),
    path('notes/', views.NoteAPIView.as_view()),
    path('notes/<int:pk>/', views.NoteDetailAPIView.as_view()),
    path('feed/', views.FeedAPIView.as_view())
]
