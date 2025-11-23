from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from rest_framework import generics
from .models_inspected import Contents
from .serializers import ContentTitleSerializer, ContentDetailSerializer
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken



class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Kayıt başarılı!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
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







