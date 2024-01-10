from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("group", views.GroupViewSet)
router.register("student", views.StudentViewSet)
router.register("file", views.FileViewSet)
router.register("readonly-entry", views.EntryReadOnlyViewSet)
router.register("entry", views.EntryViewSet)
router.register("choice", views.ChoiceViewSet)
router.register("vote", views.VoteViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("user/", views.user.as_view()),
    path("index/", views.index),
    path("single_upload/", views.single_upload),
    path("multiple_upload/", views.multiple_upload),
    path("output/", views.Output.as_view(), name="status"),
    path("group_introduction/", views.GroupText.as_view(), name="group_introduction"),
    path("weighted_result/", views.WeightedResult.as_view(), name="weighted_result"),
]
