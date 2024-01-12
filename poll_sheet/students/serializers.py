from rest_framework import serializers

from .models import Group, Student, FileModel, ImageModel, Entry, Choice, Vote


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class EntryReadOnlySerializer(serializers.ModelSerializer):
    group_index = serializers.ReadOnlyField()

    class Meta:
        model = Entry
        fields = "__all__"


class EntrySerializer(serializers.ModelSerializer):
    aggregated = serializers.ReadOnlyField()

    class Meta:
        model = Entry
        fields = "__all__"


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = "__all__"


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = "__all__"


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = "__all__"


class MultipleFileSerializer(serializers.Serializer):
    files = serializers.ListField(child=serializers.FileField())


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = "__all__"


class MultipleImageSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.ImageField())
