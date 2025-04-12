from django.urls import path
from .views import RegisterView, LoginView, BookListView, BookSearchView, BookCreateView
from rest_framework.authtoken.views import obtain_auth_token
from .views import BookDetailView
from .views import ProfileView, ProfileUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', obtain_auth_token),
    path('books/', BookListView.as_view()),
    path('books/search/', BookSearchView.as_view()),
    path('books/add/', BookCreateView.as_view()),
    path('books/<int:id>/', BookDetailView.as_view()),
    path('profile/update/', ProfileUpdateView.as_view()),
    path('profile/', ProfileView.as_view()), 
]
