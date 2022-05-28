from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import ProjectSerializer
from .models import Project, Contributor
from .permissions import ContributorReadCreateAuthorUpdateDelete


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [ContributorReadCreateAuthorUpdateDelete]

    def get_queryset(self):
        # filter the shown project to members only
        project_contributed_to = Contributor.objects.filter(user=self.request.user).values_list('project_id')
        print('filter project to members only, user:', self.request.user, project_contributed_to)
        return Project.objects.filter(id__in=project_contributed_to )