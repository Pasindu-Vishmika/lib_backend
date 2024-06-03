from django.contrib.auth.backends import ModelBackend
from .models import Librarian, Member

class MultiUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        # Try to authenticate Librarian
        try:
            librarian = Librarian.objects.get(email=username)
            if librarian.check_password(password):
                return librarian
        except Librarian.DoesNotExist:
            pass

        # Try to authenticate Member
        try:
            member = Member.objects.get(email=username)
            if member.check_password(password):
                return member
        except Member.DoesNotExist:
            pass

        return None

    def get_user(self, user_id):
        try:
            return Librarian.objects.get(pk=user_id)
        except Librarian.DoesNotExist:
            try:
                return Member.objects.get(pk=user_id)
            except Member.DoesNotExist:
                return None
