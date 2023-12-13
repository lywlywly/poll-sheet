# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


User = get_user_model()
for _ in range(1, 9):
    User.objects.create_user(
        "user{i}".format(i=_), "user{i}@duke.edu".format(i=_), "123456"
    )
