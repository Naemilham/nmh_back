from django import urls

from accounts import views

urlpatterns = [
    urls.path("signup/", views.SignupView.as_view()),
]
