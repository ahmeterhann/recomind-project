from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models_inspected import Contents   
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Favorite



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
            'content_type', 'status'
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


class IsFavoriteSerializer(serializers.Serializer):
    """
    Bir içerinin favoride olup olmadığını kontrol et
    """
    is_favorite = serializers.BooleanField()




