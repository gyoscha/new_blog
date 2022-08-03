from django.urls import path

from . import views

urlpatterns = [
    path('accounts/profile/', views.AccountAPIView.as_view()),
    path('accounts/signup/', views.CreateUserView.as_view()),
    path('notes/', views.NoteAPIView.as_view()),
    path('notes/<int:pk>/', views.NoteDetailAPIView.as_view()),
]
