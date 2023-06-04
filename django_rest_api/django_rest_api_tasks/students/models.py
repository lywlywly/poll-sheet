from django.db import models


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


class FileModel(models.Model):
    # id = models.IntegerField(primary_key=True)
    id = models.OneToOneField(Group, on_delete=models.CASCADE, primary_key=True)
    file = models.FileField(upload_to='file/')


class ImageModel(models.Model):
    file = models.ImageField(upload_to='img/')
