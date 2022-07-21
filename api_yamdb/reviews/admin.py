from django.contrib import admin

from .models import Comment, Review

reviews_models = [Comment, Review, ]
admin.site.register(reviews_models)