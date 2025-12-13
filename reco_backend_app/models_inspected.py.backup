# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class ContentPeople(models.Model):
    pk = models.CompositePrimaryKey('content_id', 'person_id', 'role')
    content = models.ForeignKey('Contents', models.DO_NOTHING)
    person = models.ForeignKey('People', models.DO_NOTHING)
    role = models.TextField()
    character_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'content_people'


class Contents(models.Model):
    tmdb_id = models.TextField(primary_key=True)
    content_type = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    title_en = models.TextField(blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    overview_en = models.TextField(blank=True, null=True)
    embedding = models.TextField(blank=True, null=True)  # This field type is a guess.
    rating = models.FloatField(blank=True, null=True)
    vote_count = models.IntegerField(blank=True, null=True)
    imdb_rating = models.FloatField(blank=True, null=True)
    release_year = models.IntegerField(blank=True, null=True)
    image_url = models.TextField(blank=True, null=True)
    genres = models.TextField(blank=True, null=True)  # This field type is a guess.
    runtime = models.IntegerField(blank=True, null=True)
    original_language = models.TextField(blank=True, null=True)
    imdb_id = models.TextField(blank=True, null=True)
    popularity = models.FloatField(blank=True, null=True)
    backdrop_url = models.TextField(blank=True, null=True)
    tagline = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    number_of_seasons = models.IntegerField(blank=True, null=True)
    number_of_episodes = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contents'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('RecoBackendAppUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class People(models.Model):
    person_id = models.TextField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    deathday = models.DateField(blank=True, null=True)
    birthplace = models.TextField(blank=True, null=True)
    profile_url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people'


class RecoBackendAppUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    email = models.CharField(unique=True, max_length=254)
    phone = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reco_backend_app_user'


class RecoBackendAppUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(RecoBackendAppUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'reco_backend_app_user_groups'
        unique_together = (('user', 'group'),)


class RecoBackendAppUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(RecoBackendAppUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'reco_backend_app_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Reviews(models.Model):
    review_id = models.TextField(primary_key=True)
    content = models.ForeignKey(Contents, models.DO_NOTHING, blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    content_0 = models.TextField(db_column='content', blank=True, null=True)  # Field renamed because of name conflict.

    class Meta:
        managed = False
        db_table = 'reviews'
