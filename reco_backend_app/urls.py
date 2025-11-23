from django.urls import path
from .views import (
    RegisterView, LoginView, MovieListView, MovieByGenreView, TvListView, 
    TvByGenreView, ProfileView, ContentDetailView, FavoriteListCreateView, 
    FavoriteDetailView, IsFavoriteView, SearchView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('movies/', MovieListView.as_view(), name='movies'),
    path('movies/by-genre/', MovieByGenreView.as_view(), name='movies_by_genre'),
    path('tv/', TvListView.as_view(), name='tv_list'),
    path('tv/by-genre/', TvByGenreView.as_view(), name='tv_by_genre'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('contents/<str:tmdb_id>/', ContentDetailView.as_view(), name='content_detail'),
    
    # Favori endpoint'leri
    path('favorites/', FavoriteListCreateView.as_view(), name='favorite_list_create'),
    path('favorites/<str:content>/', FavoriteDetailView.as_view(), name='favorite_detail'),
    path('contents/<str:tmdb_id>/is-favorite/', IsFavoriteView.as_view(), name='is_favorite'),
    
    # Arama endpoint'i
    path('search/', SearchView.as_view(), name='search'),
]