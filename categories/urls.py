from django.urls import path

from .views import (
    CategoryDetailView,
    CategoryListView,
    EmailCategoryListView,
    WriterCategoryListView,
)

urlpatterns = [
    path("", CategoryListView.as_view()),
    path("<int:pk>/", CategoryDetailView.as_view()),
    path("email/", EmailCategoryListView.as_view()),
    path("writer/", WriterCategoryListView.as_view()),
]
