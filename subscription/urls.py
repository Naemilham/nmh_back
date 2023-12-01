from django import urls

from subscription import views

urlpatterns = [
    urls.path("subscribe/", views.SubscribeView.as_view()),
    urls.path("unsubscribe/", views.UnsubscribeView.as_view()),
    urls.path("subscribing-writers/", views.SubscribingWritersListView.as_view()),
    urls.path("subscribing-readers/", views.SubscribingReadersListView.as_view()),
]
