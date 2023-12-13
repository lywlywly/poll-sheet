from students.models import Group

for i in range(1, 5):
    g = Group(id=i)
    g.save()
