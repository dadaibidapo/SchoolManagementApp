# authentication.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class RoleBasedAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                if user.role == User.Role.STUDENT:
                    if hasattr(user, 'studentprofile'):
                        return user
                elif user.role == User.Role.TEACHER:
                    if hasattr(user, 'teacherprofile'):
                        return user
        except User.DoesNotExist:
            return None
