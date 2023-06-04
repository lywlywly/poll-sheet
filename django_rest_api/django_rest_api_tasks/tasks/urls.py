from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('tasks', views.TasksViewSet)

# define the urls
urlpatterns = [
    path('', include(router.urls)),
]
