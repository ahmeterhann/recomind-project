# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Books(models.Model):
    book_id = models.TextField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    authors = models.TextField(blank=True, null=True)
    categories = models.TextField(blank=True, null=True)  # This field type is a guess.
    year = models.IntegerField(blank=True, null=True)
    pages = models.IntegerField(blank=True, null=True)
    popularity = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    description_tr = models.TextField(blank=True, null=True)
    cover_url = models.TextField(blank=True, null=True)
    embedding = models.TextField(blank=True, null=True)  # This field type is a guess.
    average_rating = models.FloatField(blank=True, null=True)
    language = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'books'


class BooksPeople(models.Model):
    book = models.ForeignKey(Books, models.DO_NOTHING, blank=True, null=True)
    person = models.ForeignKey('People', models.DO_NOTHING, blank=True, null=True)
    role = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'books_people'
        unique_together = (('book', 'person'),)


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
