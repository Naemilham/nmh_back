from rest_framework import generics

from .models import Category, EmailCategory, WriterCategory
from .serializers import (
    CategorySerializer,
    EmailCategorySerializer,
    WriterCategorySerializer,
)


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class EmailCategoryListView(generics.ListCreateAPIView):
    queryset = EmailCategory.objects.all()
    serializer_class = EmailCategorySerializer


class WriterCategoryListView(generics.ListCreateAPIView):
    queryset = WriterCategory.objects.all()
    serializer_class = WriterCategorySerializer
