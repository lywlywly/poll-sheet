from students.models import Group, Entry

g = Group.objects.all()
for _ in range(1, 5):
    Entry(group_id=g[_ - 1], text="Content", type="choices_num").save()
    Entry(group_id=g[_ - 1], text="Delivery", type="choices_num").save()
    Entry(group_id=g[_ - 1], text="Any other words", type="text").save()
