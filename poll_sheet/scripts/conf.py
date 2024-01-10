import yaml
import json

from django.contrib.auth import get_user_model
from students.models import User, Group, Entry, Student, Choice

with open("conf.yaml", "r") as f:
    document = f.read()

with open("groups.json", "r") as f:
    groups = f.read()

conf = yaml.safe_load(document)
groups = json.loads(groups)

scale = conf["rating scale questions"]["scale"]
group_cnt = len(groups)
flattened_list = [item for sublist in groups for item in sublist]
student_cnt = len(flattened_list)

# populate user
User = get_user_model()
for e in flattened_list:
    User.objects.create_user(
        e["name"], "{i}@duke.edu".format(i=e["net_id"]), e["password"]
    )

# populate group
for i in range(1, group_cnt + 1):
    g = Group(id=i)
    g.save()

# populate student
users = User.objects.all()
gs = Group.objects.all()
for index, group in enumerate(groups):
    # use `next` because there is a single match (primary key), or none
    for student in group:
        s = Student(
            # id=_,
            net_id=student["net_id"],
            user=next(
                filter(
                    lambda x: x.email == "{i}@duke.edu".format(i=student["net_id"]),
                    users,
                )
            ),
            name=student["name"],
            group_id=gs.get(id=index + 1),
        )
        s.save()

# populate group
for group_index in range(group_cnt):
    for e in conf["rating scale questions"]["items"]:
        Entry(
            group_id=gs[group_index],
            text=e["name"],
            type="choices_num",
            weight=e["weight"],
        ).save()
    for e in conf["text questions"]["items"]:
        Entry(group_id=gs[group_index], text=e, type="text").save()

# populate choice
entries = Entry.objects.all()
for e in entries:
    if e.type == "choices_num":
        for score in range(1, scale + 1):
            Choice(poll=e, choice_text=score).save()
    elif e.type == "text":
        Choice(poll=e, choice_text="Enter your words").save()
