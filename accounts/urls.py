from django import urls
from rest_framework_simplejwt import views as jwt_views

from accounts import views as accounts_views

urlpatterns = [
    urls.path("signup/", accounts_views.SignupView.as_view()),
    urls.path("signin/", accounts_views.SigninView.as_view()),
    urls.path("signout/", accounts_views.SignoutView.as_view()),
    urls.path("api/token/", jwt_views.TokenObtainPairView.as_view()),
    urls.path("api/token/refresh/", jwt_views.TokenRefreshView.as_view()),
]
