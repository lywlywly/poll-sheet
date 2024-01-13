import sys, os, django

sys.path.append("../")  # here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poll_sheet.settings")
django.setup()

import yaml
import json

from django.contrib.auth import get_user_model
from students.models import Group, Entry, Student, Choice, Poll

User = get_user_model()


# populate user
def populate_users(roaster):
    for e in roaster:
        User.objects.create_user(
            e["name"], "{i}@duke.edu".format(i=e["net_id"]), e["password"]
        )


# populate student
def populate_students(roaster):
    users = User.objects.all()
    for s in roaster:
        # use `next` because there is a single match (primary key), or none
        student = Student(
            net_id=s["net_id"],
            user=next(
                filter(
                    lambda x: x.email == "{i}@duke.edu".format(i=s["net_id"]),
                    users,
                )
            ),
            name=s["name"],
        )
        student.save()


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
        for net_id in group:
            the_group = Group.objects.get(index=index + 1, poll_id=p)
            the_group.students.add(Student.objects.get(net_id=net_id))
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
                weight=e.get("weight", 1),
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


def init(file_path):
    with open(file_path, "r") as f:
        roaster = f.read()

    roaster = json.loads(roaster)
    populate_users(roaster)
    populate_students(roaster)


def poll(config_path, group_path):
    with open(config_path, "r") as f:
        config = f.read()

    with open(group_path, "r") as f:
        roaster = f.read()

    config = yaml.safe_load(config)
    roaster = json.loads(roaster)

    scale = config["rating scale questions"]["scale"]
    group_cnt = len(roaster)
    p = create_poll(config["name"])
    populate_groups(group_cnt, p)
    assign_groups(roaster, p)
    populate_entries(config, group_cnt, p)
    populate_choices(scale, p)


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script description")

    parser.add_argument(
        "-i", "--init", type=str, help="Input json file to create users"
    )
    parser.add_argument(
        "-g", "--group", type=str, help="Input json file to create groups"
    )
    parser.add_argument("-p", "--poll", type=str, help="Input yaml file to create poll")

    args = parser.parse_args()

    if args.init:
        init(args.init)

    if args.group and args.poll:
        poll(args.poll, args.group)
