from django.urls import path

from .views import CategoryDetailView, CategoryListView

urlpatterns = [
    path("", CategoryListView.as_view()),
    path("<int:pk>/", CategoryDetailView.as_view()),
]
