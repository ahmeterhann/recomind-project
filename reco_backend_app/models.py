from django.db import models
from django.contrib.auth.models import AbstractUser
from .models_inspected import Contents



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
    


