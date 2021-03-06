from rest_framework.serializers import ModelSerializer
from .models import Project, Issue, Comment, Contributor


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = [
            "id",
            "user",
            "project",
            "role",
            "permission",
        ]


class ProjectSerializer(ModelSerializer):

    contributors = ContributorSerializer(source="contributor_project", many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["id", "author_user", "title", "description", "type", "contributors"]
        read_only_fields = ["author_user", "contributors"]

    def create(self, validated_data):
        # create project instance w/o request user
        project = Project.objects.create(**validated_data)
        # get & update user fields with request user
        project.author_user = self.context["request"].user
        # manage the external relation btw project & members, here the owner
        Contributor.objects.create(
            user=project.author_user,
            project=project,
            role=Contributor.AUTHOR,
            permission=Contributor.CREATE_READ_UPDATE_DELETE,
        )
        project.save()
        return project


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "id",
            "project",
            "author_user",
            "assignee_user",
            "title",
            "description",
            "tag",
            "priority",
            "status",
            "created_time",
        ]


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "issue",
            "author_user",
            "description",
            "created_time",
        ]
