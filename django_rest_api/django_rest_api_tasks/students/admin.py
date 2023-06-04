from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Student, Group, FileModel, Scores, GroupScore, Entry, Choice, Vote

admin.site.register(Group)
admin.site.register(Student)
admin.site.register(FileModel)
admin.site.register(GroupScore)
admin.site.register(Scores)
admin.site.register(Entry)
admin.site.register(Choice)
admin.site.register(Vote)