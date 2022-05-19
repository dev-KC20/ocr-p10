# users/urls.py
from django.urls import path, include
from rest_framework import routers

from .views import ProjectViewSet

router = routers.SimpleRouter()
router.register('projects', ProjectViewSet, basename='projects')


urlpatterns = [
    path('', include(router.urls)) 
]