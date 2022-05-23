from rest_framework.serializers import ModelSerializer

from .models import Project, Issue, Comment, Contributor

from django.contrib.auth import get_user_model
User = get_user_model()


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ["author_users", "title", "description", "type", "author"]


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ["project",
                  "author_user",
                  "assignee_user",
                  "title",
                  "description",
                  "tag",
                  "priority",
                  "status",
                  "created_time", ]


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["issue",
                  "author_user",
                  "description",
                  "created_time", ]


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["user",
                  "project",
                  "role",
                  "permission", ]
