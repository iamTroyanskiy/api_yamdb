from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.generics import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import (
    Category,
    Genre,
    Comment,
    Review,
    Title
)

User = get_user_model()


class TitleDefault:

    requires_context = True

    def __call__(self, serializer_field):
        view = serializer_field.context['view']
        title_id = view.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title


class ReviewSerializer(serializers.ModelSerializer):

    title = serializers.HiddenField(
        default=TitleDefault()
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'score', 'pub_date', 'author', 'title')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author'),
                message=(
                    'Нельзя просто так взять и добавить ещё один отзыв '
                    'на это же произведение.'
                )
            )
        ]


class CommentSerializer(serializers.ModelSerializer):

    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'pub_date', 'author', 'review')


class CategorySerializers(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializers(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesReadSerializers(serializers.ModelSerializer):
    category = CategorySerializers(read_only=True)
    genre = GenreSerializers(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleWriteSerializers(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'
