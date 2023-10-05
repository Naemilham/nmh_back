from django import urls

from accounts import views

urlpatterns = [
    urls.path("signup/", views.SignupView.as_view()),
    urls.path("/", views.UserListView.as_view()),
    urls.path("/info/", views.UserInfoView.as_view()),
]
