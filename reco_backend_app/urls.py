from django.urls import path
from .views import (
    RegisterView, LoginView, MovieListView, MovieByGenreView, TvListView, 
    TvByGenreView, ProfileView, ContentDetailView, FavoriteListCreateView, 
    FavoriteDetailView, IsFavoriteView, SearchView, ContentReviewListCreateView,
    ContentReviewDetailView, GenreListView, ContentCastView,
    BookListView, BookByCategoryView, BookDetailView, BookAuthorsView, BookCategoryListView,
    BookFavoriteListCreateView, BookFavoriteDetailView, IsBookFavoriteView,
    BookReviewListCreateView, BookReviewDetailView,
    SendFriendRequestView, FriendRequestListView, AcceptFriendRequestView,
    RejectFriendRequestView, FriendsListView, RemoveFriendView, SearchUsersView
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
    path('contents/<str:tmdb_id>/cast/', ContentCastView.as_view(), name='content_cast'),
    
    # Kitap endpoint'leri
    path('books/', BookListView.as_view(), name='books'),
    path('books/by-category/', BookByCategoryView.as_view(), name='books_by_category'),
    path('books/categories/', BookCategoryListView.as_view(), name='book_categories'),
    path('books/<str:book_id>/', BookDetailView.as_view(), name='book_detail'),
    path('books/<str:book_id>/authors/', BookAuthorsView.as_view(), name='book_authors'),

    # Favori endpoint'leri
    path('favorites/', FavoriteListCreateView.as_view(), name='favorite_list_create'),
    path('favorites/<str:content>/', FavoriteDetailView.as_view(), name='favorite_detail'),
    path('contents/<str:tmdb_id>/is-favorite/', IsFavoriteView.as_view(), name='is_favorite'),
    path('contents/<str:tmdb_id>/reviews/', ContentReviewListCreateView.as_view(), name='content_reviews'),
    path('contents/<str:tmdb_id>/reviews/<int:pk>/', ContentReviewDetailView.as_view(), name='content_review_detail'),
    path('book-favorites/', BookFavoriteListCreateView.as_view(), name='book_favorite_list_create'),
    path('book-favorites/<str:book>/', BookFavoriteDetailView.as_view(), name='book_favorite_detail'),
    path('books/<str:book_id>/is-favorite/', IsBookFavoriteView.as_view(), name='is_book_favorite'),
    path('books/<str:book_id>/reviews/', BookReviewListCreateView.as_view(), name='book_reviews'),
    path('books/<str:book_id>/reviews/<int:pk>/', BookReviewDetailView.as_view(), name='book_review_detail'),
    
    # Arama endpoint'i
    path('search/', SearchView.as_view(), name='search'),
    
    # Genre listesi endpoint'i
    path('genres/', GenreListView.as_view(), name='genres'),
    
    # Arkadaşlık endpoint'leri
    path('friends/', FriendsListView.as_view(), name='friends_list'),
    path('friends/request/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('friends/requests/', FriendRequestListView.as_view(), name='friend_requests'),
    path('friends/requests/<int:pk>/accept/', AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path('friends/requests/<int:pk>/reject/', RejectFriendRequestView.as_view(), name='reject_friend_request'),
    path('friends/<int:pk>/', RemoveFriendView.as_view(), name='remove_friend'),
    path('users/search/', SearchUsersView.as_view(), name='search_users'),
]