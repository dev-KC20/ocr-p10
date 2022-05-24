from rest_framework.serializers import ModelSerializer, CharField, SlugRelatedField,StringRelatedField

from .models import Project, Issue, Comment, Contributor

# from django.contrib.auth import get_user_model

# User = get_user_model()


class ContributorSerializer(ModelSerializer):
    
    class Meta:
        model = Contributor
        fields = [
                  "user",
                  "project",
                  "role",
                  "permission", ]


class ProjectSerializer(ModelSerializer):

    contributors = ContributorSerializer(source='contributor_project', many=True, read_only=True)
    # contributors = ContributorSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["author_users", "title", "description", "type", "contributors"]
        read_only_fields = ['author_users', 'contributors']

    def create(self, validated_data):
        # create project instance w/o request user
        project = Project.objects.create(**validated_data)
        # get & update user fields with request user
        project.author_users = self.context['request'].user
        # manage the external relation btw project & members, here the owner
        Contributor.objects.create(
            user=project.author_users,
            project=project,
            role=Contributor.AUTHOR,
            permission=Contributor.CREATE_READ_UPDATE_DELETE
        )
        project.save()
        return project

    # def get_contributors(self, instance):
    #     queryset = instance.contributors.all()
    #     serializer = ContributorSerializer(queryset, many=True)
    #     return serializer.data

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
