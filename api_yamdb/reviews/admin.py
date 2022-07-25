from django.contrib import admin

from .models import Category, Genre, Title
from .models import Comment, Review

reviews_models = [Comment, Review, ]
admin.site.register(reviews_models)

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



