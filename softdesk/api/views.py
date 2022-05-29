from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import ProjectSerializer, ContributorSerializer
from .models import Project, Contributor
from .permissions import ContributorReadCreateAuthorUpdateDelete

User = get_user_model()


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [ContributorReadCreateAuthorUpdateDelete]

    def get_queryset(self):
        # filter the shown project to members only
        # Project.objects.filter(contributor__user=self.request.user)
        project_contributed_to = Contributor.objects.filter(user=self.request.user).values_list('project_id')
        print('filter project to members only, user:', self.request.user, project_contributed_to)
        return Project.objects.filter(id__in=project_contributed_to)


class ContributorViewSet(ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [ContributorReadCreateAuthorUpdateDelete]

    def get_queryset(self):
        # filter the shown project to members only
        project_id = self.kwargs.get('project_id')
        print('get_queryset project_id:', project_id)
        if project_id:

            ContributorsQueryset = Contributor.objects.filter(project=project_id, user=self.request.user)
        print('filter members only, user:', self.request.user, ContributorsQueryset)
        return ContributorsQueryset

    def perform_create(self, serializer, *args, **kwargs):
        # body of target data to be created
        create_data = self.request.data
        # print('create contributor data: ', create_data)
        target_project_id = create_data['project']
        target_user_id = create_data['user']
        # current project in the url
        project_id = self.kwargs.get('project_id')
        # owasp : do not temper with project in the data
        if project_id != target_project_id:
            error_message = f"you are not allowed to work with project {target_project_id}, pls select: {project_id}"
            raise ValidationError(error_message)
        # get the author from Project rather than from Contributor
        if not Project.objects.filter(pk=target_project_id, author_users=self.request.user).exists():
            error_message = f"you are not the owner of project {target_project_id}, pls select another."
            raise ValidationError(error_message)
        target_user = User.objects.get(pk=target_user_id)
        if not target_user:
            error_message = f"user {target_user_id} has to signup before you can add him to project {target_project_id}."
            raise ValidationError(error_message)
        if Contributor.objects.filter(project_id=target_project_id, user_id=target_user_id).exists():
            error_message = f"user {target_user_id} is already member of project {target_project_id}, pls select another."
            raise ValidationError(error_message)

        serializer.save(user=target_user, project_id=target_project_id, role=Contributor.MEMBER,
                        permission=Contributor.CREATE_READ)
        print(f"user {target_user_id} added to project {target_project_id}!")
