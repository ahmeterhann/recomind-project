from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status, permissions, serializers
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, FavoriteSerializer, IsFavoriteSerializer
from rest_framework import generics
from .models_inspected import Contents
from .serializers import ContentTitleSerializer, ContentDetailSerializer, ContentReviewSerializer
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import User, Favorite, ContentReview
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Kayıt başarılı!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "Giriş başarılı!",
                    "username": user.username,
                    "email": user.email,
                    "access": str(refresh.access_token),      # Access token
                    "refresh": str(refresh), 
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieListView(generics.ListAPIView):
    serializer_class = ContentTitleSerializer

    def get_queryset(self):
        return Contents.objects.filter(content_type__iexact="movie").order_by('title')

class MovieByGenreView(generics.ListAPIView):
    serializer_class = ContentTitleSerializer

    def get_queryset(self):
        genres = self.request.query_params.getlist("genre")  
        

        if not genres:
            return Contents.objects.none()

        
        query = Q()

        
        for genre in genres:
            query |= Q(genres__icontains=genre)

        
        return Contents.objects.filter(
            content_type__iexact="movie"
        ).filter(query).order_by("title")

class TvListView(generics.ListAPIView):
    serializer_class = ContentTitleSerializer

    def get_queryset(self):
        return Contents.objects.filter(
            content_type__iexact="tv"
        ).order_by("title")


class TvByGenreView(generics.ListAPIView):
    serializer_class = ContentTitleSerializer

    def get_queryset(self):
        genres = self.request.query_params.getlist("genre")  
        # Ör: ["Comedy", "Drama"]

        if not genres:
            return Contents.objects.none()

        q = Q()
        for genre in genres:
            q |= Q(genres__icontains=genre)

        return Contents.objects.filter(
            content_type__iexact="tv"
        ).filter(q).order_by("title")


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Kullanıcı profil bilgilerini getir ve güncelle
    GET: /profile/ - Giriş yapan kullanıcının profil bilgilerini döndür
    PUT/PATCH: /profile/ - Profil bilgilerini güncelle
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class ContentDetailView(generics.RetrieveAPIView):
    queryset = Contents.objects.all()
    serializer_class = ContentDetailSerializer
    lookup_field = 'tmdb_id'


class FavoriteListCreateView(generics.ListCreateAPIView):
    """
    Favorileri listele ve yeni favori ekle
    GET: Kullanıcının tüm favorilerini döndür
    POST: İçeriği favorilere ekle
    """
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class FavoriteDetailView(generics.DestroyAPIView):
    """
    Favorilerden çıkar
    DELETE: İçeriği favorilerden sil
    """
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'content'

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class IsFavoriteView(generics.GenericAPIView):
    """
    Bir içerinin favoride olup olmadığını kontrol et
    GET: /contents/<tmdb_id>/is-favorite/
    """
    permission_classes = [IsAuthenticated]
    serializer_class = IsFavoriteSerializer

    def get(self, request, tmdb_id):
        try:
            favorite = Favorite.objects.get(user=request.user, content__tmdb_id=tmdb_id)
            return Response({"is_favorite": True})
        except Favorite.DoesNotExist:
            return Response({"is_favorite": False})


class SearchView(generics.ListAPIView):
    """
    Film ve dizi arama
    GET: /search/?q=inception&content_type=movie
    Parameters:
        - q: Aranacak kelime (zorunlu)
        - content_type: "movie" veya "tv" (opsiyonel)
    """
    serializer_class = ContentTitleSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        q = self.request.query_params.get('q', '').strip()
        content_type = self.request.query_params.get('content_type', None)

        if not q or len(q) < 1:
            return Contents.objects.none()

        # Başlık veya açıklamada arama yap
        query = Q(title__icontains=q) | Q(overview__icontains=q)
        
        # İçerik tipi filtresi (opsiyonel)
        if content_type in ['movie', 'tv']:
            query &= Q(content_type__iexact=content_type)

        return Contents.objects.filter(query).order_by('-rating', '-vote_count')


class IsReviewOwnerOrReadOnly(permissions.BasePermission):
    """
    Yorum sahibinin düzenleme/silme yapmasına izin ver
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class ContentReviewListCreateView(generics.ListCreateAPIView):
    """
    Bir içerik için yorum/puan listele ve yeni kayıt oluştur
    """
    serializer_class = ContentReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return ContentReview.objects.filter(content__tmdb_id=self.kwargs['tmdb_id']).select_related('user')

    def perform_create(self, serializer):
        content = get_object_or_404(Contents, tmdb_id=self.kwargs['tmdb_id'])
        user = self.request.user
        if ContentReview.objects.filter(user=user, content=content).exists():
            raise serializers.ValidationError("Bu içerik için zaten yorumunuz bulunuyor.")
        serializer.save(user=user, content=content)


class ContentReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Tekil yorum için görüntüle/güncelle/sil işlemleri
    """
    serializer_class = ContentReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewOwnerOrReadOnly]
    lookup_field = 'pk'

    def get_queryset(self):
        return ContentReview.objects.filter(content__tmdb_id=self.kwargs['tmdb_id']).select_related('user')


class GenreListView(generics.GenericAPIView):
    """
    Film veya dizi için mevcut genre listesini döndür
    GET: /genres/?content_type=movie veya /genres/?content_type=tv
    """
    permission_classes = [AllowAny]

    def get(self, request):
        import json
        content_type = request.query_params.get('content_type', '').lower()
        
        if content_type not in ['movie', 'tv']:
            return Response(
                {"error": "content_type parametresi 'movie' veya 'tv' olmalıdır."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Veritabanından ilgili içerikleri çek
        contents = Contents.objects.filter(content_type__iexact=content_type)
        
        # Tüm unique genre'leri topla
        all_genres = set()
        for content in contents:
            if content.genres:
                # Genre'leri parse et
                if isinstance(content.genres, list):
                    genres_list = content.genres
                else:
                    try:
                        genres_list = json.loads(content.genres)
                        if not isinstance(genres_list, list):
                            genres_list = [g.strip() for g in content.genres.split(',') if g.strip()]
                    except:
                        genres_list = [g.strip() for g in content.genres.split(',') if g.strip()]
                
                # Genre'leri set'e ekle
                for genre in genres_list:
                    if genre and genre.strip():
                        all_genres.add(genre.strip())
        
        # Alfabetik sırala ve döndür
        sorted_genres = sorted(list(all_genres))
        return Response({"genres": sorted_genres}, status=status.HTTP_200_OK)








