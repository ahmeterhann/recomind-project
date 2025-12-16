from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models_inspected import Contents, People, ContentPeople, Books, BooksPeople
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Favorite, ContentReview, BookFavorite, BookReview
from django.db.models import Avg, Count



User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'password',
            'phone', 'birth_date', 'gender', 'country'
        ]

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data['email'],
            phone=validated_data.get('phone', ''),
            birth_date=validated_data.get('birth_date', None),
            gender=validated_data.get('gender', ''),
            country=validated_data.get('country', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # Email ile kullanıcıyı bul
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("E-posta veya şifre hatalı.")

        # Şifre doğru mu kontrol et
        if not user.check_password(password):
            raise serializers.ValidationError("E-posta veya şifre hatalı.")

        attrs["user"] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    """
    Kullanıcı profil bilgilerini serialize et
    """
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'phone', 'birth_date', 'gender', 'country', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']

class ContentTitleSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    
    def get_genres(self, obj):
        """Parse genres string to list"""
        if not obj.genres:
            return []
        if isinstance(obj.genres, list):
            return obj.genres
        # Try to parse JSON string
        import json
        try:
            parsed = json.loads(obj.genres)
            return parsed if isinstance(parsed, list) else []
        except:
            # Fallback: split by comma
            return [g.strip() for g in obj.genres.split(',') if g.strip()]
    
    class Meta:
        model = Contents
        fields = [
            'tmdb_id',
            'title',
            'image_url',
            'release_year',
            'rating',
            'vote_count',
            'genres',
            'content_type',
        ]

class ContentDetailSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    latest_reviews = serializers.SerializerMethodField()
    
    def get_genres(self, obj):
        """Parse genres string to list"""
        if not obj.genres:
            return []
        if isinstance(obj.genres, list):
            return obj.genres
        # Try to parse JSON string
        import json
        try:
            parsed = json.loads(obj.genres)
            return parsed if isinstance(parsed, list) else []
        except:
            # Fallback: split by comma
            return [g.strip() for g in obj.genres.split(',') if g.strip()]
    
    class Meta:
        model = Contents
        fields = [
            'tmdb_id', 'title', 'overview', 'genres', 'release_year', 'image_url',
            'rating', 'vote_count', 'imdb_rating', 'runtime', 'original_language',
            'tagline', 'number_of_seasons', 'number_of_episodes', 'backdrop_url',
            'content_type', 'status', 'average_rating', 'rating_count', 'latest_reviews'
        ]

    def get_average_rating(self, obj):
        aggregate = obj.content_reviews.aggregate(avg=Avg('rating'))
        return aggregate['avg'] or 0.0

    def get_rating_count(self, obj):
        return obj.content_reviews.count()

    def get_latest_reviews(self, obj):
        reviews = obj.content_reviews.select_related('user').order_by('-created_at')[:5]
        return ContentReviewSerializer(reviews, many=True).data


class BookTitleSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    authors = serializers.SerializerMethodField()

    def _parse_list_field(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return value
        import json
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return parsed
        except Exception:
            pass
        return [v.strip() for v in str(value).split(',') if v.strip()]

    def get_categories(self, obj):
        return self._parse_list_field(obj.categories)

    def get_authors(self, obj):
        return self._parse_list_field(obj.authors)

    class Meta:
        model = Books
        fields = [
            'book_id',
            'title',
            'cover_url',
            'year',
            'average_rating',
            'categories',
            'authors',
            'pages',
            'language',
            'popularity',
        ]


class BookReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    comment = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = BookReview
        fields = ['id', 'user', 'book', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'book']

    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Puan 1 ile 10 arasında olmalıdır.")
        return value


class BookDetailSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    authors = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    latest_reviews = serializers.SerializerMethodField()

    def _parse_list_field(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return value
        import json
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return parsed
        except Exception:
            pass
        return [v.strip() for v in str(value).split(',') if v.strip()]

    def get_categories(self, obj):
        return self._parse_list_field(obj.categories)

    def get_authors(self, obj):
        return self._parse_list_field(obj.authors)

    def get_description(self, obj):
        return obj.description_tr or obj.description

    def get_average_rating(self, obj):
        aggregate = obj.book_reviews.aggregate(avg=Avg('rating'))
        return aggregate['avg'] or obj.average_rating or 0.0

    def get_rating_count(self, obj):
        return obj.book_reviews.count()

    def get_latest_reviews(self, obj):
        reviews = obj.book_reviews.select_related('user').order_by('-created_at')[:5]
        return BookReviewSerializer(reviews, many=True).data

    class Meta:
        model = Books
        fields = [
            'book_id',
            'title',
            'cover_url',
            'year',
            'pages',
            'popularity',
            'description',
            'average_rating',
            'rating_count',
            'latest_reviews',
            'categories',
            'authors',
            'language',
            'embedding',
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Kullanıcının favorilerine içerik ekle/çıkar
    """
    content_detail = ContentTitleSerializer(source='content', read_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'content', 'content_detail', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        # Giriş yapan kullanıcıyı otomatik ata
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class BookFavoriteSerializer(serializers.ModelSerializer):
    """
    Kullanıcının favorilerine kitap ekle/çıkar
    """
    book_detail = BookTitleSerializer(source='book', read_only=True)

    class Meta:
        model = BookFavorite
        fields = ['id', 'book', 'book_detail', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class IsFavoriteSerializer(serializers.Serializer):
    """
    Bir içerinin favoride olup olmadığını kontrol et
    """
    is_favorite = serializers.BooleanField()


class ContentReviewSerializer(serializers.ModelSerializer):
    """
    Yorum ve puan verisini serialize eder
    """
    user = serializers.StringRelatedField(read_only=True)
    comment = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = ContentReview
        fields = ['id', 'user', 'content', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'content']

    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Puan 1 ile 10 arasında olmalıdır.")
        return value


class ContentReviewSummarySerializer(serializers.Serializer):
    """
    İçerik detayında gösterilecek özet istatistikler
    """
    average_rating = serializers.FloatField()
    rating_count = serializers.IntegerField()


class PersonSerializer(serializers.ModelSerializer):
    """
    Oyuncu bilgilerini serialize eder
    """
    class Meta:
        model = People
        fields = [
            'person_id',
            'name',
            'profile_url',
            'biography',
            'birthday',
            'birthplace'
        ]


class ContentPeopleSerializer(serializers.ModelSerializer):
    """
    Film/Dizi ile oyuncu ilişkisini serialize eder
    """
    person = PersonSerializer(read_only=True)
    
    class Meta:
        model = ContentPeople
        fields = [
            'person',
            'role',
            'character_name'
        ]


class BookPeopleSerializer(serializers.ModelSerializer):
    """
    Kitap ile yazar ilişkisini serialize eder
    """
    person = PersonSerializer(read_only=True)

    class Meta:
        model = BooksPeople
        fields = [
            'person',
            'role'
        ]



