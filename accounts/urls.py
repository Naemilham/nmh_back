from django import urls
from rest_framework_simplejwt import views as jwt_views

from accounts import views as accounts_views

urlpatterns = [
    urls.path("signup/", accounts_views.SignupView.as_view()),
    urls.path("signin/", accounts_views.SigninView.as_view()),
    urls.path("signout/", accounts_views.SignoutView.as_view()),
    urls.path(
        "send-verification-email/", accounts_views.SendVerificationEmailView.as_view()
    ),
    urls.path(
        "resend-verification-email/<int:pk>/",
        accounts_views.ResendVerificationEmailView.as_view(),
    ),
    urls.path("verify-email/<int:pk>/", accounts_views.VerifyEmailView.as_view()),
    urls.path("writers/", accounts_views.WriterListView().as_view()),
    urls.path("readers/", accounts_views.ReaderListView().as_view()),
    urls.path("api/token/", jwt_views.TokenObtainPairView.as_view()),
    urls.path("api/token/refresh/", jwt_views.TokenRefreshView.as_view()),
    urls.path("info/<int:pk>/", accounts_views.UserInfoView.as_view()),
    urls.path("users/", accounts_views.AllUsersListView.as_view()),
]
