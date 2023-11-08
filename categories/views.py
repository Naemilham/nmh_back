from rest_framework import APIView, status
from rest_framework.response import Response

from .models import Category
from .serializers import CategorySerializer


class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        return Response(status=status.HTTP_200_OK, data=categories)


class CategoryDetailView(APIView):
    def post(self, request):
        category_name = request.data.get("category_name")

        if category_name is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
