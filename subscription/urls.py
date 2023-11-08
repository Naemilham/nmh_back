from django import urls

from subscription import views

urlpatterns = [
    urls.path("subscribe/", views.SubscribeView.as_view()),
]
