from rest_framework import generics

from .models import Category
from .serializers import CategorySerializer


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
