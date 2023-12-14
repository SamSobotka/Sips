from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

UserModel = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # print(UserModel)
        # print(username)
        # print(password)
        try:
            user = UserModel.objects.get(Q(handle__iexact=username) | Q(email__iexact=username))
            # print(user.userid)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return
        except UserModel.MultipleObjectsReturned:
            user = UserModel.objects.filter(Q(handle__iexact=username) | Q(email__iexact=username)).order_by('userid').first()

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
