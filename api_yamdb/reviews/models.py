from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models



class Review(models.Model):
    """Модель отзывы."""

    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    text = models.TextField(verbose_name='Отзыв')
    author = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'Поставьте рейтинг от 1 до 10'),
            MaxValueValidator(10, 'Поставьте рейтинг от 1 до 10'),
        ],
        verbose_name='Рейтинг',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'), name='distinct_review'
            ),
        ]

    def __str__(self):
        return self.text[:42]


class Comment(models.Model):
    """Модель комментарии."""

    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )
    text = models.TextField(
        verbose_name='Комментарий',
    )
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:42]

