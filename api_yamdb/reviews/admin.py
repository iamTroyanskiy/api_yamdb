from django.contrib import admin

from .models import (
    Category,
    Genre,
    Title,
    Comment,
    Review
)


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenresAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitlesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'category')
    search_fields = ('name',)
    list_filter = ('name', )
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )
    search_fields = ('review',)
    list_filter = ('review',)
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'author',
        'score',
    )
    search_fields = ('pub_date',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
