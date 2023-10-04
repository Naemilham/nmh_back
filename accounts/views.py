from dj_rest_auth.registration import views as dj_reg_views


class SignupView(dj_reg_views.RegisterView):
    pass


# TODO: define UserDetailView for retrieve, update, delete user info using dj_rest_auth
class UserDetailView(dj_reg_views.UserDetailsView):
    def get(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass
