from students.models import Group, Student
from django.contrib.auth import get_user_model
import random

User = get_user_model()
a = User.objects.all()
g = Group.objects.all()

for _ in range(1, 9):
    # use `next` because there is a single match (primary key), or none
    r = int(random.random() * 4) + 1
    s = Student(
        id=_,
        net_id="00{i}".format(i=_),
        user=next(filter(lambda x: x.username == "user{i}".format(i=_), a)),
        name="student{i}".format(i=_),
        group_id=g[r - 1],
    )
    s.save()
