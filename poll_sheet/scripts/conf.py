import yaml
import json

from django.contrib.auth import get_user_model
from students.models import Group, Entry, Student, Choice, Poll

with open("conf.yaml", "r") as f:
    document = f.read()

with open("groups.json", "r") as f:
    roaster = f.read()

config = yaml.safe_load(document)
roaster = json.loads(roaster)

scale = config["rating scale questions"]["scale"]
group_cnt = len(roaster)
flattened_list = [item for sublist in roaster for item in sublist]
student_cnt = len(flattened_list)
User = get_user_model()


# populate user
def populate_users(flattened_list):
    for e in flattened_list:
        User.objects.create_user(
            e["name"], "{i}@duke.edu".format(i=e["net_id"]), e["password"]
        )


# populate student
def populate_students(groups):
    users = User.objects.all()
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
                # group_id=gs.get(id=index + 1),
            )
            s.save()


# create a poll
def create_poll(name):
    p = Poll(name=name)
    p.save()
    return p


# populate group
def populate_groups(group_cnt, p):
    for i in range(1, group_cnt + 1):
        g = Group(index=i, poll_id=p)
        g.save()


# assign groups
def assign_groups(groups, p):
    for index, group in enumerate(groups):
        for student in group:
            the_group = Group.objects.get(index=index + 1, poll_id=p)
            the_group.students.add(Student.objects.get(net_id=student["net_id"]))
            the_group.save()


# populate entry
def populate_entries(conf, group_cnt, p):
    for group_index in range(group_cnt):
        for e in conf["rating scale questions"]["items"]:
            print(Group.objects.all())
            print(group_index + 1)
            print(p)
            Entry(
                group_id=Group.objects.get(index=group_index + 1, poll_id=p),
                text=e["name"],
                type="choices_num",
                weight=e["weight"],
            ).save()
        for e in conf["text questions"]["items"]:
            Entry(
                group_id=Group.objects.get(index=group_index + 1, poll_id=p),
                text=e,
                type="text",
            ).save()


# populate choice
def populate_choices(scale, p):
    entries = Entry.objects.all().filter(group_id__poll_id=p)
    for e in entries:
        if e.type == "choices_num":
            for score in range(1, scale + 1):
                Choice(poll=e, choice_text=score).save()
        elif e.type == "text":
            Choice(poll=e, choice_text="Enter your words").save()


def init():
    populate_users(flattened_list)
    populate_students(roaster)


def poll():
    p = create_poll(config["name"])
    populate_groups(group_cnt, p)
    assign_groups(roaster, p)
    populate_entries(config, group_cnt, p)
    populate_choices(scale, p)


# init()
poll()
