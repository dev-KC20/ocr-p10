from rest_framework.serializers import ModelSerializer
 
from .models import Project
 
from django.contrib.auth import get_user_model
User = get_user_model()


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'
