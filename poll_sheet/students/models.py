from django.db import models
from django.db.models.aggregates import Avg
from django.db.models.constraints import UniqueConstraint, CheckConstraint
from django.contrib.auth.models import User
from accounts.models import CustomUser
from django.db.models import Q


class Poll(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    expiring = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    net_id = models.TextField(blank=True, null=True)
    # group_id = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.net_id


class Group(models.Model):
    index = models.IntegerField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return "id:" + str(self.id)


class Entry(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)

    @property
    def aggregated(self):
        filtered_votes = Vote.objects.filter(choice__poll=self.id)
        if self.type == "choices_num":
            li = list(map(lambda x: int(x.choice.choice_text), filtered_votes))
            return sum(li) / len(li) if len(li) > 0 else "NaN"
        elif self.type == "text":
            li = list(map(lambda x: x.content, filtered_votes))
            return li

    @property
    def group_index(self):
        return self.group_id.index

    def __str__(self):
        return str(self.group_id.id) + self.text


class Choice(models.Model):
    poll = models.ForeignKey(Entry, on_delete=models.CASCADE)
    choice_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.poll) + " " + str(self.choice_text)


class Vote(models.Model):
    # class Meta:
    #     constraints = [
    #         UniqueConstraint(fields=["voter", "entry"], name="unique_blocking"),
    #     ]

    voter = models.ForeignKey(Student, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)

    # def __str__(self):
    #     return str(self.voter.id) + " " + str(self.entry.id)


class FileModel(models.Model):
    id = models.OneToOneField(Group, on_delete=models.CASCADE, primary_key=True)
    file = models.FileField(upload_to="file/")


class ImageModel(models.Model):
    file = models.ImageField(upload_to="img/")
