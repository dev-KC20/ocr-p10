from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer
from .models import Project, Contributor, Issue
from .permissions import ContributorReadCreateAuthorUpdateDelete
from django.urls import resolve
from django.shortcuts import get_object_or_404


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
        # filter the url shown project to members only
        print('get_queryset kwargs:', self.kwargs)
        project_id = self.kwargs.get('project_pk')
        contributor_pk = self.kwargs.get('pk')
        print('get_queryset kwargs project/users:', project_id, contributor_pk)
        if contributor_pk and project_id:
            # queryset = super().get_queryset().filter(project=project_id, user=contributor_pk)
            queryset = Contributor.objects.filter(project=project_id, user_id=contributor_pk)
            print('get_queryset pk:', queryset)
            self.kwargs['pk'] = queryset.values_list('id')[0][0]
            print('get_queryset kwargs:', self.kwargs)
        elif project_id:
            queryset = Contributor.objects.filter(project=project_id)
            print('get_queryset project:', queryset)

        return queryset

    def destroy(self, request, *args, **kwargs):
        print('retrieve kwargs:', self.kwargs)
        contributor_to_delete = get_object_or_404(self.get_queryset())
        self.check_object_permissions(self.request, contributor_to_delete)
        self.perform_destroy(contributor_to_delete)
        message = 'The contributor was successfully removed from project '
        return Response({'message': message}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        print('retrieve kwargs:', self.kwargs)
        contributor = get_object_or_404(self.get_queryset())
        serializer = ContributorSerializer(contributor)
        return Response(serializer.data)

    def perform_create(self, serializer, *args, **kwargs):
        # body of target data to be created
        create_data = self.request.data
        print('create contributor data: ', create_data)
        target_project_id = create_data['project']
        target_user_id = create_data['user']
        # current project in the url
        project_id = self.kwargs.get('project_pk')
        print('create contributor url: ', self.kwargs, project_id, target_project_id)
        # owasp : do not temper with project in the data
        if not(int(project_id) == int(target_project_id)):
            print('nothing to do here')
            error_message = f"you are not allowed to work with project {target_project_id}, pls select: {project_id}"
            raise ValidationError(error_message)
        # get the author from Project rather than from Contributor
        if not Project.objects.filter(pk=target_project_id, author_user=self.request.user).exists():
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



class IssueViewSet(ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [ContributorReadCreateAuthorUpdateDelete]

    def get_queryset(self):
        # filter the url shown project to members only
        print('get_queryset kwargs:', self.kwargs)
        project_id = self.kwargs.get('project_pk')
        issue_pk = self.kwargs.get('pk')
        print('get_queryset kwargs project/issues:', project_id, issue_pk)
        if issue_pk and project_id:
            queryset = Issue.objects.filter(project=project_id, id=issue_pk)
            print('get_queryset pk:', queryset)
            self.kwargs['pk'] = queryset.values_list('id')[0][0]
            print('get_queryset kwargs:', self.kwargs)
        elif project_id:
            queryset = Issue.objects.filter(project=project_id)
            print('get_queryset project:', queryset)

        return queryset


    def perform_create(self, serializer, *args, **kwargs):
        # body of target data to be created
        create_data = self.request.data
        print('create issue data: ', create_data)
        target_project_id = create_data['project']
        target_author_id = create_data['author_user']
        target_assignee_id = create_data['assignee_user']
        # current project in the url
        project_id = self.kwargs.get('project_pk')
        print('create issue url: ', self.kwargs, project_id, target_project_id)
        # the logged user needs to be member of the project
        if not Contributor.objects.filter(project_id=target_project_id, user_id=self.request.user).exists():
            error_message = f"You, user {self.request.user} need to be member of project {target_project_id}, pls work with your projects."
            raise ValidationError(error_message)

        # owasp : do not temper with project in the data
        if not(int(project_id) == int(target_project_id)):
            print('nothing to do here')
            error_message = f"you are not allowed to work with project {target_project_id}, pls select: {project_id}"
            raise ValidationError(error_message)

        target_assignee = User.objects.get(pk=target_assignee_id)
        if not target_assignee:
            error_message = f"user {target_assignee_id} has to signup before you can add him to project {target_project_id}."
            raise ValidationError(error_message)

        if not Contributor.objects.filter(project_id=target_project_id, user_id=target_assignee_id).exists():
            error_message = f"user {target_assignee_id} needs to be member of project {target_project_id}, pls add him to project before."
            raise ValidationError(error_message)

        # serializer.save(user=target_user, project_id=target_project_id, role=Issue.MEMBER,
        #                 permission=Issue.CREATE_READ)
        super().perform_create(serializer, *args, **kwargs)
        print(f"issue added to project {target_project_id}!")
    
    
    # def destroy(self, request, *args, **kwargs):
    #     print('retrieve kwargs:', self.kwargs)
    #     contributor_to_delete = get_object_or_404(self.get_queryset())
    #     self.check_object_permissions(self.request, contributor_to_delete)
    #     self.perform_destroy(contributor_to_delete)
    #     message = 'The contributor was successfully removed from project '
    #     return Response({'message': message}, status=status.HTTP_204_NO_CONTENT)

    # def retrieve(self, request, *args, **kwargs):
    #     print('retrieve kwargs:', self.kwargs)
    #     contributor = get_object_or_404(self.get_queryset())
    #     serializer = ContributorSerializer(contributor)
    #     return Response(serializer.data)