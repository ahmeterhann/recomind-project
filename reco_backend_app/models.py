from django.db import models
from django.contrib.auth.models import AbstractUser
from .models_inspected import Contents, Books
from django.core.validators import MinValueValidator, MaxValueValidator



class User(AbstractUser):

    email = models.EmailField(unique=True)  # E-posta benzersiz olacak
    phone = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    
    GENDER_CHOICES = [
        ('M', 'Erkek'),
        ('F', 'Kadın'),
        ('O', 'Diğer'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.username


class Favorite(models.Model):
    """
    Kullanıcıların favori film/dizi/kitap kaydı
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    content = models.ForeignKey(Contents, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content')  # Bir kullanıcı aynı içeriği 2 kez favori yapamaz
        ordering = ['-created_at']  # Yeni eklenenler ilk

    def __str__(self):
        return f"{self.user.username} - {self.content.title}"
    

class ContentReview(models.Model):
    """
    Kullanıcıların içeriklere puan verip yorum bırakmasını sağlar
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_reviews')
    content = models.ForeignKey(Contents, on_delete=models.CASCADE, related_name='content_reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'content')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.content.title} ({self.rating}/10)"


class BookFavorite(models.Model):
    """
    Kullanıcıların favori kitap kayıtları
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_favorites')
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"


class BookReview(models.Model):
    """
    Kullanıcıların kitaplara puan verip yorum bırakmasını sağlar
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_reviews')
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='book_reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'book')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.rating}/10)"
