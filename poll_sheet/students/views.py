from functools import reduce
from django.forms import ValidationError
from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Group, Student, FileModel, ImageModel, Entry, Choice, Vote, Poll
from rest_framework.views import APIView
from .permissions import IsStaff, IsVoter, IsAuthorOrReadOnly
from .serializers import (
    EntryReadOnlySerializer,
    GroupSerializer,
    StudentSerializer,
    FileSerializer,
    MultipleFileSerializer,
    ImageSerializer,
    MultipleImageSerializer,
    EntrySerializer,
    ChoiceSerializer,
    VoteSerializer,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from django.db.models import F
import pandas as pd
from django.http import HttpResponse
from io import BytesIO
from rest_framework import permissions


# Create your views here.

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


def find_elements_not_in_list(all_items, my_items):
    elements_not_in_my_items = [
        element for element in all_items if element not in my_items
    ]
    return len(elements_not_in_my_items) > 0


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.request.query_params
        if find_elements_not_in_list(query_params, ["poll_id"]):
            raise ValidationError("unknown query parameters")
        filter_param = query_params.get("poll_id")
        if filter_param:
            queryset = queryset.filter(poll_id=filter_param)
        return queryset

    # def list(self, request):
    #     query_params = request.query_params
    #     if find_elements_not_in_list(query_params, ["poll_id"]):
    #         return Response(
    #             "Unknown query parameters", status=status.HTTP_400_BAD_REQUEST
    #         )

    #     filter_param = query_params.get("poll_id")
    #     if filter_param:
    #         queryset = self.queryset.filter(poll_id=filter_param)

    #     return Response(GroupSerializer(queryset, many=True).data)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class EntryReadOnlyViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntryReadOnlySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_param = self.request.query_params.get("poll_id")
        print(filter_param)
        if filter_param:
            queryset = queryset.filter(group_id__poll_id=filter_param)
        return queryset


class EntryViewSet(viewsets.ModelViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (IsStaff,)
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class StudentGroup(APIView):
    def get(self, request):
        filter_param = request.query_params.get("poll_id")
        student_id = request.query_params.get("student_id")
        return get_student_group(student_id, filter_param)


def get_student_group(student_id, poll_id):
    try:
        group = Group.objects.filter(poll_id=poll_id, students__id=student_id).first()
        if group:
            return group
    except Group.DoesNotExist:
        pass

    return None


class VoteViewSet(viewsets.ModelViewSet):
    permission_classes = (IsVoter,)
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def list(self, request):
        filter_param = self.request.query_params.get("poll_id")
        if request.user.is_staff:
            queryset_all = Vote.objects.all()
            serializer_all = VoteSerializer(queryset_all, many=True)
            return Response(serializer_all.data)
        queryset = (
            Vote.objects.all()
            .filter(voter_id=request.user.student.id)
            .filter(choice__poll__group_id__poll_id=filter_param)
        )
        serializer = VoteSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()
        # print(request.user)
        # print(request.user.student.id)
        request_data["voter"] = (
            request.user.student.id if request.user.is_authenticated else None
        )
        poll_id = request_data["poll_id"]
        choice_id = int(request.data["choice"])
        choice = Choice.objects.get(id=choice_id)
        poll = Entry.objects.get(id=choice.poll.id)
        myVotes = Vote.objects.filter(voter=request.user.student)
        # choice=choice_id for same choice
        if len(myVotes.filter(choice__poll=poll)) != 0:
            return Response(
                "You already have voted for the same entry",
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            get_student_group(request.user.student.id, poll_id).index
            == Entry.objects.get(pk=choice.poll.id).group_id.index
        ):
            return Response(
                "You cannot vote for the same group as you",
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


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
            files_list.append(FileModel(file=file))
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
            images_list.append(ImageModel(file=image))
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


class user(APIView):
    def get(self, request):
        print(request.user)
        # print(request.META)
        poll_id = request.query_params.get("poll_id")
        print(request.user.user_permissions.all())

        response = {
            "id": request.user.id,
            "username": request.user.username,
        }

        if hasattr(request.user, "email"):
            response["email"] = request.user.email

        if hasattr(request.user, "student"):
            response["group"] = get_student_group(
                request.user.student.id, poll_id
            ).index

        if request.user.is_staff:
            response["status"] = "staff"

        return Response(response)


class GroupText(APIView):
    def post(self, request):
        request_data = request.data
        # request.data is by default string
        group_index = int(request_data.get("group_index"))
        poll_id = int(request_data.get("poll_id"))
        if get_student_group(request.user.student.id, poll_id).index != group_index:
            return HttpResponse("Not in the group", status=403)
        text = request_data.get("text")

        g = Group.objects.get(index=group_index, poll_id=poll_id)
        g.text = text
        g.save()

        return Response("success")

    def get(self, request):
        group_id = request.query_params.get("group_id")

        g = Group.objects.get(id=group_id)

        response_json = {"text": g.text}

        return Response(response_json)


class WeightedResult(APIView):
    permission_classes = (IsStaff,)

    def get(self, request):
        entries = EntrySerializer(Entry.objects.all(), many=True).data
        print(entries)
        grouped_entries = reduce(
            lambda acc, entry: acc.update(
                {entry["group_id"]: acc.get(entry["group_id"], []) + [entry]}
            )
            # FIXME:python lambda must be expression, ugly solution here
            or acc,
            entries,
            {},
        )

        def aggregate_weighted(entries):
            r = reduce(
                lambda acc, curr: acc
                + (
                    curr["aggregated"] * curr["weight"]
                    if curr["type"] == "choices_num" and curr["aggregated"] != "NaN"
                    else 0
                ),
                entries,
                0.0,
            )
            total_weights = reduce(
                lambda acc, curr: acc
                + (curr["weight"] if curr["type"] == "choices_num" else 0),
                entries,
                0.0,
            )
            return r / total_weights

        weighted_result = [aggregate_weighted(i[1]) for i in grouped_entries.items()]

        return Response(weighted_result)


class Output(APIView):
    permission_classes = (IsStaff,)

    def get(self, request):
        # "format" is a reserved Django Rest Framework keyword
        type = request.query_params.get("type", "json")

        result = Vote.objects.values(
            "id",
            "content",
            entry_type=F("choice__poll__type"),
            entry_text=F("choice__poll__text"),
            entry_group_id=F("choice__poll__group_id_id"),
            choice_text=F("choice__choice_text"),
            voter_name=F("voter__name"),
            voter_net_id=F("voter__net_id"),
            voter_group_id=F("voter__group_id_id"),
        )

        if type == "xlsx":
            df = pd.DataFrame(result)

            buffer = BytesIO()

            writer = pd.ExcelWriter(buffer, engine="openpyxl")
            df.to_excel(writer, index=False)
            writer.close()

            buffer.seek(0)

            response = HttpResponse(
                buffer,
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = "attachment; filename=my_data.xlsx"

            return response

        return Response(result)
