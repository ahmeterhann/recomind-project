# RecoMind - İçerik Öneri Sistemi

## 📋 Proje Hakkında

RecoMind, film ve dizi içeriklerini keşfetmek, favorilere eklemek ve değerlendirmek için geliştirilmiş bir Django REST Framework tabanlı web API projesidir. Bu proje, bitirme ödevi kapsamında geliştirilmiş olup aktif olarak geliştirilmeye devam etmektedir.

## 🎯 Özellikler

- **Kullanıcı Yönetimi**: Kayıt, giriş ve profil yönetimi
- **İçerik Keşfi**: Film ve dizi listeleme, detay görüntüleme
- **Filtreleme**: Tür bazlı içerik filtreleme
- **Favori Sistemi**: İçerikleri favorilere ekleme ve çıkarma
- **Değerlendirme Sistemi**: İçeriklere puan verme ve yorum yapma
- **Arama**: Film ve dizi arama özelliği
- **JWT Authentication**: Güvenli token tabanlı kimlik doğrulama

## 🛠️ Teknolojiler

- Django 5.2.1
- Django REST Framework
- PostgreSQL
- JWT (JSON Web Token)
- Django CORS Headers


## 📚 API Endpoints

### Kimlik Doğrulama
- `POST /register/` - Kullanıcı kaydı
- `POST /login/` - Kullanıcı girişi
- `POST /token/refresh/` - Token yenileme

### Profil
- `GET /profile/` - Profil bilgilerini getir
- `PUT /profile/` - Profil bilgilerini güncelle
- `PATCH /profile/` - Profil bilgilerini kısmi güncelle

### İçerikler
- `GET /movies/` - Tüm filmleri listele
- `GET /movies/by-genre/?genre=Action&genre=Drama` - Tür bazlı film filtreleme
- `GET /tv/` - Tüm dizileri listele
- `GET /tv/by-genre/?genre=Comedy` - Tür bazlı dizi filtreleme
- `GET /contents/<tmdb_id>/` - İçerik detaylarını getir
- `GET /search/?q=inception&content_type=movie` - İçerik arama

### Favoriler
- `GET /favorites/` - Kullanıcının favorilerini listele
- `POST /favorites/` - Favorilere içerik ekle
- `DELETE /favorites/<content>/` - Favorilerden içerik çıkar
- `GET /contents/<tmdb_id>/is-favorite/` - İçeriğin favoride olup olmadığını kontrol et

### Yorumlar ve Puanlar
- `GET /contents/<tmdb_id>/reviews/` - İçerik yorumlarını listele
- `POST /contents/<tmdb_id>/reviews/` - Yeni yorum ve puan ekle
- `GET /contents/<tmdb_id>/reviews/<pk>/` - Yorum detayını getir
- `PUT /contents/<tmdb_id>/reviews/<pk>/` - Yorumu güncelle
- `DELETE /contents/<tmdb_id>/reviews/<pk>/` - Yorumu sil

## 🔐 Kimlik Doğrulama

API'yi kullanmak için JWT token gereklidir. Login endpoint'inden aldığınız `access` token'ı, isteklerinizde `Authorization` header'ında kullanın:

```
Authorization: Bearer <your_access_token>
```

## 📝 Notlar

- Bu proje bitirme ödevi kapsamında geliştirilmiştir
- Proje aktif olarak geliştirilmeye devam etmektedir
- Production ortamında kullanmadan önce güvenlik ayarlarını gözden geçirin


## 📦 Kurulum

### Gereksinimler
- Python 3.8+
- PostgreSQL
- pip

### Adımlar

1. **Projeyi klonlayın:**
   ```bash
   git clone <repository-url>
   cd recomind
   ```

2. **Sanal ortam oluşturun ve aktifleştirin:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Bağımlılıkları yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

4. **PostgreSQL veritabanını oluşturun ve `settings.py` dosyasındaki veritabanı ayarlarını güncelleyin**

5. **Veritabanı migrasyonlarını çalıştırın:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Sunucuyu başlatın:**
   ```bash
   python manage.py runserver
   ```

API artık `http://localhost:8000/` adresinde çalışıyor olacaktır.
