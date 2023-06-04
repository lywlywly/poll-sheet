from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Student, Group, FileModel

admin.site.register(Group)
admin.site.register(Student)
admin.site.register(FileModel)
