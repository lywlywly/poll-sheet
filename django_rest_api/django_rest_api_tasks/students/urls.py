from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('group', views.GroupViewSet)
router.register('student', views.StudentViewSet)
router.register('file', views.FileViewSet)
router.register('score', views.ScoreViewSet)
router.register('scores', views.ScoresViewSet)
router.register('entry', views.EntryViewSet)
router.register('choice', views.ChoiceViewSet)
router.register('vote', views.VoteViewSet)

# urlpatterns = [
#     path("", views.index, name="index"),
# ]


urlpatterns = [
    path('', include(router.urls)),
    path('index/', views.index),
    path('single_upload/', views.single_upload),
    path('multiple_upload/', views.multiple_upload),
]
