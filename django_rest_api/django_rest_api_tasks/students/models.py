from django.db import models
from django.db.models.aggregates import Avg
from django.db.models.constraints import UniqueConstraint


class Group(models.Model):
    id = models.IntegerField(primary_key=True)
    score = models.FloatField()

    def __str__(self):
        # return the task title
        return 'id:' + str(self.id)


# Create your models here.
class Student(models.Model):
    # title
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    net_id = models.TextField(blank=True, null=True)
    # group_id = models.IntegerField()
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        # return the task title
        return self.net_id


class GroupScore(models.Model):
    # titlevote
    id = models.OneToOneField(Group, on_delete=models.CASCADE, primary_key=True)
    delivery = models.IntegerField()
    content = models.IntegerField()


class Scores(models.Model):
    # title
    id = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
    group_scores = models.ManyToManyField(GroupScore)


class Entry(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    entry_score = models.IntegerField()

    @property
    def computed(self):
        # return Jobs.objects.filter(person_id_id=self.person_id_id).first().job_income_in_usd * 0.89
        return Vote.objects.filter(entry_id=self.id).all().aggregate(Avg("selection"))

    def __str__(self):
        # return the task title
        return str(self.group_id.id) + self.text


class Choice(models.Model):
    poll_id = models.ForeignKey(Entry, on_delete=models.CASCADE)
    selection = models.IntegerField()


class Vote(models.Model):
    class Meta:
        constraints = [
            UniqueConstraint(fields=['voter', 'entry'], name='unique_blocking')
        ]

    voter = models.ForeignKey(Student, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    selection = models.IntegerField()
    # choice = models.ForeignKey(Choice, on_delete=models.CASCADE)


class FileModel(models.Model):
    # id = models.IntegerField(primary_key=True)
    id = models.OneToOneField(Group, on_delete=models.CASCADE, primary_key=True)
    file = models.FileField(upload_to='file/')


class ImageModel(models.Model):
    file = models.ImageField(upload_to='img/')
