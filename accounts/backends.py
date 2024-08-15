from django.contrib.auth.backends import ModelBackend
from accounts.models import User

class IdentityNoBackend(ModelBackend):
    def authenticate(self, request, identity_no=None, password=None, **kwargs):
        try:
            user = User.objects.get(identity_no=identity_no)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None