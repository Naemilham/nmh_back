from rest_framework import serializers

from .models import Category, EmailCategory, WriterCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class EmailCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailCategory
        fields = "__all__"


class WriterCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WriterCategory
        fields = "__all__"
