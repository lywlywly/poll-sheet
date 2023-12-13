from students.models import Group, Entry

g = Group.objects.all()
for _ in range(1, 5):
    Entry(group_id=g[_ - 1], text="Engagement", type="choices_num").save()
