from allauth.account.adapter import DefaultAccountAdapter


class UserAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, False)
        data = form.cleaned_data
        user.is_writer = data.get("is_writer")
        user.is_reader = data.get("is_reader")

        if commit:
            user.save()

        return user
