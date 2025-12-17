from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status, permissions, serializers
from rest_framework.response import Response
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
    FavoriteSerializer,
    IsFavoriteSerializer,
    BookFavoriteSerializer,
    BookTitleSerializer,
    BookDetailSerializer,
    BookReviewSerializer,
    BookPeopleSerializer,
    FriendshipSerializer,
    UserSearchSerializer,
)
from rest_framework import generics
from .models_inspected import Contents, ContentPeople, Books, BooksPeople
from .serializers import ContentTitleSerializer, ContentDetailSerializer, ContentReviewSerializer, ContentPeopleSerializer
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import User, Favorite, ContentReview, BookFavorite, BookReview, Friendship
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


class BookListView(generics.ListAPIView):
    serializer_class = BookTitleSerializer

    def get_queryset(self):
        return Books.objects.all().order_by("title")


class BookByCategoryView(generics.ListAPIView):
    serializer_class = BookTitleSerializer

    def get_queryset(self):
        categories = self.request.query_params.getlist("category")
        if not categories:
            return Books.objects.none()

        q = Q()
        for category in categories:
            q |= Q(categories__icontains=category)

        return Books.objects.filter(q).order_by("title")


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


class BookDetailView(generics.RetrieveAPIView):
    queryset = Books.objects.all()
    serializer_class = BookDetailSerializer
    lookup_field = 'book_id'


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


class BookFavoriteListCreateView(generics.ListCreateAPIView):
    """
    Kitap favorilerini listele ve yeni favori ekle
    """
    serializer_class = BookFavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BookFavorite.objects.filter(user=self.request.user)


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


class BookFavoriteDetailView(generics.DestroyAPIView):
    """
    Kitabı favorilerden çıkar
    """
    serializer_class = BookFavoriteSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'book'

    def get_queryset(self):
        return BookFavorite.objects.filter(user=self.request.user)


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


class IsBookFavoriteView(generics.GenericAPIView):
    """
    Bir kitabın favoride olup olmadığını kontrol et
    GET: /books/<book_id>/is-favorite/
    """
    permission_classes = [IsAuthenticated]
    serializer_class = IsFavoriteSerializer

    def get(self, request, book_id):
        try:
            BookFavorite.objects.get(user=request.user, book__book_id=book_id)
            return Response({"is_favorite": True})
        except BookFavorite.DoesNotExist:
            return Response({"is_favorite": False})


class SearchView(generics.GenericAPIView):
    """
    Film, dizi ve kitap arama (birleşik)
    GET: /search/?q=inception&content_type=movie|tv|book
    """
    permission_classes = [AllowAny]

    def get(self, request):
        q = request.query_params.get('q', '').strip()
        content_type = request.query_params.get('content_type', None)

        if not q or len(q) < 1:
            return Response({"results": [], "count": 0})

        results = []

        if content_type is None or content_type in ['movie', 'tv']:
            contents_query = Q(title__icontains=q) | Q(overview__icontains=q)
            if content_type in ['movie', 'tv']:
                contents_query &= Q(content_type__iexact=content_type)

            contents = Contents.objects.filter(contents_query).order_by('-rating', '-vote_count')[:20]
            for content in contents:
                results.append({
                    "type": "content",
                    "data": ContentTitleSerializer(content).data
                })

        if content_type is None or content_type == 'book':
            books_query = Q(title__icontains=q) | Q(description__icontains=q) | Q(authors__icontains=q)
            books = Books.objects.filter(books_query).order_by('-average_rating', '-popularity')[:20]
            for book in books:
                results.append({
                    "type": "book",
                    "data": BookTitleSerializer(book).data
                })

        return Response({"results": results, "count": len(results)})


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


class BookReviewListCreateView(generics.ListCreateAPIView):
    """
    Bir kitap için yorum/puan listele ve yeni kayıt oluştur
    """
    serializer_class = BookReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return BookReview.objects.filter(book__book_id=self.kwargs['book_id']).select_related('user')

    def perform_create(self, serializer):
        book = get_object_or_404(Books, book_id=self.kwargs['book_id'])
        user = self.request.user
        if BookReview.objects.filter(user=user, book=book).exists():
            raise serializers.ValidationError("Bu kitap için zaten yorumunuz bulunuyor.")
        serializer.save(user=user, book=book)


class ContentReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Tekil yorum için görüntüle/güncelle/sil işlemleri
    """
    serializer_class = ContentReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewOwnerOrReadOnly]
    lookup_field = 'pk'

    def get_queryset(self):
        return ContentReview.objects.filter(content__tmdb_id=self.kwargs['tmdb_id']).select_related('user')


class BookReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Tekil kitap yorumu için görüntüle/güncelle/sil işlemleri
    """
    serializer_class = BookReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewOwnerOrReadOnly]
    lookup_field = 'pk'

    def get_queryset(self):
        return BookReview.objects.filter(book__book_id=self.kwargs['book_id']).select_related('user')


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


class BookCategoryListView(generics.GenericAPIView):
    """
    Kitaplar için mevcut kategori listesini döndür
    GET: /books/categories/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        import json
        books = Books.objects.all()
        all_categories = set()
        for book in books:
            if book.categories:
                if isinstance(book.categories, list):
                    categories_list = book.categories
                else:
                    try:
                        categories_list = json.loads(book.categories)
                        if not isinstance(categories_list, list):
                            categories_list = [c.strip() for c in str(book.categories).split(',') if c.strip()]
                    except Exception:
                        categories_list = [c.strip() for c in str(book.categories).split(',') if c.strip()]
                for category in categories_list:
                    if category and str(category).strip():
                        all_categories.add(str(category).strip())
        sorted_categories = sorted(list(all_categories))
        return Response({"categories": sorted_categories}, status=status.HTTP_200_OK)


class ContentCastView(generics.ListAPIView):
    """
    Bir film/dizi için oyuncu kadrosunu döndürür
    GET: /contents/<tmdb_id>/cast/
    Query Parameters:
        - role: Rol filtresi (örn: "actor", "director") - opsiyonel
    """
    serializer_class = ContentPeopleSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        tmdb_id = self.kwargs['tmdb_id']
        role = self.request.query_params.get('role', None)
        
        # İçeriğin var olup olmadığını kontrol et
        content = get_object_or_404(Contents, tmdb_id=tmdb_id)
        
        queryset = ContentPeople.objects.filter(
            content__tmdb_id=tmdb_id
        ).select_related('person', 'content')
        
        # Rol filtresi (opsiyonel)
        if role:
            queryset = queryset.filter(role__iexact=role)
        
        # Oyuncuları önce role göre, sonra karakter adına göre sırala
        return queryset.order_by('role', 'character_name')


class BookAuthorsView(generics.ListAPIView):
    """
    Bir kitap için yazar listesini döndürür
    GET: /books/<book_id>/authors/
    """
    serializer_class = BookPeopleSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        get_object_or_404(Books, book_id=book_id)
        queryset = BooksPeople.objects.filter(
            book__book_id=book_id
        ).select_related('person', 'book')
        return queryset.order_by('role', 'person__name')


class SendFriendRequestView(generics.CreateAPIView):
    """
    Arkadaşlık isteği gönder
    POST: /friends/request/
    Body: {"receiver_username": "kullanici_adi"}
    """
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        receiver_username = request.data.get('receiver_username')
        
        if not receiver_username:
            return Response(
                {"error": "receiver_username gerekli"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            return Response(
                {"error": "Kullanıcı bulunamadı"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        if receiver == request.user:
            return Response(
                {"error": "Kendinize arkadaşlık isteği gönderemezsiniz"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Zaten arkadaşlık isteği var mı kontrol et
        existing = Friendship.objects.filter(
            (Q(requester=request.user, receiver=receiver) | 
             Q(requester=receiver, receiver=request.user))
        ).first()
        
        if existing:
            if existing.status == 'accepted':
                return Response(
                    {"error": "Zaten arkadaşsınız"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif existing.status == 'pending':
                if existing.requester == request.user:
                    return Response(
                        {"error": "Zaten arkadaşlık isteği gönderdiniz"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    # Karşı taraftan gelen isteği otomatik kabul et
                    existing.status = 'accepted'
                    existing.save()
                    serializer = self.get_serializer(existing)
                    return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Yeni istek oluştur
        friendship = Friendship.objects.create(
            requester=request.user,
            receiver=receiver,
            status='pending'
        )
        serializer = self.get_serializer(friendship)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FriendRequestListView(generics.ListAPIView):
    """
    Gelen arkadaşlık isteklerini listele
    GET: /friends/requests/
    """
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Friendship.objects.filter(
            receiver=self.request.user,
            status='pending'
        ).select_related('requester', 'receiver')


class AcceptFriendRequestView(generics.UpdateAPIView):
    """
    Arkadaşlık isteğini kabul et
    PATCH: /friends/requests/<id>/accept/
    """
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Friendship.objects.filter(
            receiver=self.request.user,
            status='pending'
        )

    def patch(self, request, *args, **kwargs):
        friendship = self.get_object()
        friendship.status = 'accepted'
        friendship.save()
        serializer = self.get_serializer(friendship)
        return Response(serializer.data)


class RejectFriendRequestView(generics.UpdateAPIView):
    """
    Arkadaşlık isteğini reddet
    PATCH: /friends/requests/<id>/reject/
    """
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Friendship.objects.filter(
            receiver=self.request.user,
            status='pending'
        )

    def patch(self, request, *args, **kwargs):
        friendship = self.get_object()
        friendship.status = 'rejected'
        friendship.save()
        return Response({"message": "Arkadaşlık isteği reddedildi"})


class FriendsListView(generics.ListAPIView):
    """
    Arkadaş listesini getir
    GET: /friends/
    """
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Friendship.objects.filter(
            (Q(requester=self.request.user) | Q(receiver=self.request.user)),
            status='accepted'
        ).select_related('requester', 'receiver')


class RemoveFriendView(generics.DestroyAPIView):
    """
    Arkadaşlığı kaldır
    DELETE: /friends/<id>/
    """
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Friendship.objects.filter(
            (Q(requester=self.request.user) | Q(receiver=self.request.user)),
            status='accepted'
        )


class SearchUsersView(generics.ListAPIView):
    """
    Kullanıcı ara
    GET: /users/search/?q=kullanici_adi
    """
    serializer_class = UserSearchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '').strip()
        if not query or len(query) < 2:
            return User.objects.none()
        
        return User.objects.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        ).exclude(id=self.request.user.id)[:20]






