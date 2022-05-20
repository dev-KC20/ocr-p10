# not passing and spending too much time while no great knowledge on APITest
# renamed
from django.urls import reverse_lazy, reverse, path, include
from rest_framework.test import APITestCase, URLPatternsTestCase

from .models import Project


class ApiAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):

        cls.project = Project.objects.create(title='Ananas', type='B')
        Project.objects.create(title='Banane', type='F')

        cls.project_2 = Project.objects.create(title='Tomate', type='B')

    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class TestProject(ApiAPITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]
    url = reverse('projects-list')

    def get_project_detail_data(self, projects):
        return [
            {
                'id': project.pk,
                'title': project.title,
                'type': project.type,
            } for project in projects
        ]

    def test_list(self):
        response = self.client.get(reverse('projects-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_project_detail_data([self.project, self.project_2]), response.json())

    def test_create(self):
        project_count = Project.objects.count()
        response = self.client.post(reverse('projects-list'), data={'title': 'Nouvelle catégorie', 'type': 'A'})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Project.objects.count(), project_count)

    def test_delete(self):
        response = self.client.delete(reverse('projects-list', kwargs={'pk': self.project.pk}))
        self.assertEqual(response.status_code, 405)
        self.project.refresh_from_db()
