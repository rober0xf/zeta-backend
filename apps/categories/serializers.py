from rest_framework import serializers
from .models import Category


# converts the models information and converts it to json format
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "views"]
