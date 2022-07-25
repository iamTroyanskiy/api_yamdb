from django.db import models

from .validators import validate_year


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=256
    )
    slug = models.SlugField(
        'Slug категории',
        max_length=50,
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} {self.name}'


class Genre(models.Model):
    name = models.CharField(
        'Название жанра',
        max_length=256
    )
    slug = models.SlugField(
        'Slug жанра',
        max_length=50,
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name} {self.name}'


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=256,
        db_index=True

    )
    year = models.IntegerField(
        'Год выпуска',
        validators=[validate_year],
    )
    description = models.TextField(
        'Описание',
        max_length=200
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
