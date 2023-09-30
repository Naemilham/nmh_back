from dj_rest_auth import views as dj_auth_views
from dj_rest_auth.registration import views as dj_reg_views


class SignupView(dj_reg_views.RegisterView):
    pass


class SigninView(dj_auth_views.LoginView):
    pass


class SignoutView(dj_auth_views.LogoutView):
    pass
