from rest_framework import serializers
from rest_framework.serializers import Serializer, FileField

from .models import Group, Student, FileModel, ImageModel


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = "__all__"


class MultipleFileSerializer(serializers.Serializer):
    files = serializers.ListField(
        child=serializers.FileField()
    )


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = "__all__"


class MultipleImageSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.ImageField()
    )
