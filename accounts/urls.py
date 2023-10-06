from django import urls

from accounts import views

urlpatterns = [
    urls.path("signup/", views.SignupView.as_view()),
    urls.path("writers/", views.WriterListView().as_view()),
    urls.path("readers/", views.ReaderListView().as_view()),
    urls.path("info/", views.UserInfoView.as_view()),
]
