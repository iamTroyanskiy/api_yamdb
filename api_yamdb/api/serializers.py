from rest_framework import serializers

from reviews.models import Category, Genre, Title


class CategorySerializers(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializers(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


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
