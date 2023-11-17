from django.urls import path

from .views import CategoryDetailView, CategoryListView

urlpatterns = [
    path("", CategoryListView.as_view()),
    path("<int:category_id>/", CategoryDetailView.as_view()),
]
