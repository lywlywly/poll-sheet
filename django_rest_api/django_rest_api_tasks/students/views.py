from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Group, Student, FileModel, ImageModel, GroupScore, Scores, Entry, Choice, Vote
from .serializers import GroupSerializer, StudentSerializer, FileSerializer, MultipleFileSerializer, ImageSerializer, \
    MultipleImageSerializer, ScoreSerializer, ScoresSerializer, EntrySerializer, ChoiceSerializer, VoteSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse


# Create your views here.

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = GroupScore.objects.all()
    serializer_class = ScoreSerializer


class ScoresViewSet(viewsets.ModelViewSet):
    queryset = Scores.objects.all()
    serializer_class = ScoresSerializer


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

    # def savesum(self, request):
    #     first = 5
    #     second = 6
    #     model1 = Model1(first=first, second=second)
    #     model1.save()
    #
    #     # then sum the values and save it to the second model
    #     sum = first + second
    #     model2 = Model2(Model1=model1, sum=sum)
    #     model2.save()


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


class FileViewSet(viewsets.ModelViewSet):
    queryset = FileModel.objects.all()
    serializer_class = FileSerializer

    @action(detail=False, methods=["POST"])
    def multiple_upload(self, request, *args, **kwargs):
        """Upload multiple files and create objects."""
        serializer = MultipleFileSerializer(data=request.data or None)
        serializer.is_valid(raise_exception=True)
        files = serializer.validated_data.get("files")

        files_list = []
        for file in files:
            files_list.append(
                FileModel(file=file)
            )
        if files_list:
            FileModel.objects.bulk_create(files_list)

        return Response("Success")


class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer

    @action(detail=False, methods=["POST"])
    def multiple_upload(self, request, *args, **kwargs):
        """Upload multiple images and create objects."""
        serializer = MultipleImageSerializer(data=request.data or None)
        serializer.is_valid(raise_exception=True)
        images = serializer.validated_data.get("images")

        images_list = []
        for image in images:
            images_list.append(
                ImageModel(file=image)
            )
        if images_list:
            ImageModel.objects.bulk_create(images_list)

        return Response("Success")


# WITHOUT DRF UPLOADS

def single_upload(request):
    file = request.FILES.get("file")
    FileModel.objects.create(file=file)
    return JsonResponse({"message": "Success"})


def multiple_upload(request):
    files = request.FILES.getlist("files")

    files_list = []
    for file in files:
        files_list.append(FileModel(file=file))

    if files_list:
        FileModel.objects.bulk_create(files_list)

    return JsonResponse({"message": "Success"})


def index(request):
    return render(template_name="index.html", request=request)
