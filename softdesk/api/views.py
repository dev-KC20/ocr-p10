from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import ProjectSerializer
from .models import Project
from .permissions import ContributorReadCreateAuthorUpdateDelete


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [ContributorReadCreateAuthorUpdateDelete]

