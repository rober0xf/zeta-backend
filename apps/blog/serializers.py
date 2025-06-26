from rest_framework import serializers
from .models import Post
from apps.categories.serializers import CategorySerializer


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # this is bc category is a foreign key so we need to serialize it

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "thumbnail",
            "content",
            "published",
            "description",
            "views",
            "category",
        ]


class PostListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "thumbnail",
            "published",
            "description",
            "views",
            "category",
        ]
