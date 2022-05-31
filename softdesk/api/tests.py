from django.urls import reverse_lazy, reverse, path, include
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase, APIClient

from .models import Project, Contributor


User = get_user_model()


class ApiAPITestCase(APITestCase):

    @classmethod
    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class TestProject(ApiAPITestCase):

    def setUp(self):
        email = "usertest@mail.fr"
        password = "password-oc"
        self.user = User.objects.create_user(email, password)

        jwt_fetch_data = {
            'email': email,
            'password': password
        }

        url = reverse('login')
        response = self.client.post(url, jwt_fetch_data, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_jwt_signup(self):

        url = reverse('signup')

        # signup user pass
        response = self.client.post(url, {'email': 'usertest2@mail.fr', 'password': 'pass'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # signup same user fails
        response = self.client.post(url, {'email': 'usertest2@mail.fr', 'password': 'pass'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_jwt_login(self):

        url = reverse('login')
        response = self.client.post(url, {'email': 'usertest@mail.fr', 'password': 'password-oc'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)

    def test_jwt_bearer_credentials(self):

        verification_url = '/api/v1/projects/'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'abc')
        response = self.client.get(verification_url, data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(verification_url, data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
                                                       type="F", author_user=self.user)
        manually_created_contributor = Contributor.objects.create(user=self.user,
                                                                  project=newly_created_project,
                                                                  role=Contributor.AUTHOR,
                                                                  permission=Contributor.CREATE_READ_UPDATE_DELETE)
        url = reverse('projects-detail', kwargs=({'pk': newly_created_project.pk}))
        # url = '/api/v1/projects/1/'
        data = {
            "title": "Second Test Project updated",
            "description": " Long description of second updated test project",
            "type": "B"
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
