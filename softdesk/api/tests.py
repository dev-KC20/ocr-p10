# not passing and spending too much time while no great knowledge on APITest
# renamed
from django.urls import reverse_lazy, reverse, path, include
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from .models import Project


class ApiAPITestCase(APITestCase):

    @classmethod
    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class TestProject(ApiAPITestCase):

    def test_get_can_read_project_list(self):
        url = reverse('projects-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_can_create_project(self):
        url = reverse('projects-list')
        project_number_before_create = Project.objects.count()
        data = {
            "title": "First Test Project",
            "description": " Long description of first test project",
            "type": "B",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        project_number_after_create = Project.objects.count()
        self.assertEqual(project_number_before_create + 1, project_number_after_create)

    def test_put_can_update_project(self):
        # create first to know existing pk to then update
        newly_created_project = Project.objects.create(title="Second Test Project",
                                                       description=" Long description of second test project",
                                                       type="F",)
        print('pk of newly created project: ', newly_created_project.pk)
        url = reverse('projects-detail',kwargs=({'pk': newly_created_project.pk}))
        # url = '/api/v1/projects/1/'
        print('reversed url of project to be modified: ', url )
        data = {
            "title": "Second Test Project updated",
            "description": " Long description of second updated test project",
            "type": "B",
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def get_project_detail_data(self, projects):
    #     return [
    #         {
    #             'id': project.pk,
    #             'title': project.title,
    #             'type': project.type,
    #         } for project in projects
    #     ]
    # def test_list(self):
    #     self.assertEqual(response.status_code, 200)
        # self.assertEqual(self.get_project_detail_data([self.project, self.project_2]), response.json())

    # def test_create(self):
    #     project_count = Project.objects.count()
    #     response = self.client.post(reverse('projects-list'), data={'title': 'Nouvelle catégorie', 'type': 'A'})
    #     self.assertEqual(response.status_code, 405)
    #     self.assertEqual(Project.objects.count(), project_count)

    # def test_delete(self):
    #     response = self.client.delete(reverse('projects-list', kwargs={'pk': self.project.pk}))
    #     self.assertEqual(response.status_code, 405)
    #     self.project.refresh_from_db()
