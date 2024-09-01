from django.test import TestCase
from unittest.mock import patch
from apps.users.models import User
from apps.users.serializers import UserListSerializer
from rest_framework.test import APIClient
from django.urls import reverse
from apps.projects.models import Project
from apps.users.choices.positions import Positions


class UserTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='testuser1', email='test1@example.com')
        cls.user2 = User.objects.create(username='testuser2', email='test2@example.com')

    def test_get_all_users(self):
        client = APIClient()
        response = client.get(reverse('users-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_users_by_project_name(self):
        client = APIClient()
        project_name = 'example_project'

        # Создание проекта и добавление пользователя в проект
        project = Project.objects.create(name=project_name)
        self.user1.project = project
        self.user1.save()

        response = client.get(reverse('users-list'), {'project_name': project_name})
        self.assertEqual(response.status_code, 200)

    def test_get_empty_users_list(self):
        client = APIClient()
        with patch('apps.users.models.User.objects.all', return_value=[]):
            response = client.get(reverse('users-list'))
            self.assertEqual(response.status_code, 204)
            self.assertEqual(response.data, [])

    def test_user_serializer(self):
        users = [self.user1, self.user2]
        serialized_data = UserListSerializer(users, many=True).data
        for i, user in enumerate(users):
            self.assertEqual(serialized_data[i]['username'], user.username)
            self.assertEqual(serialized_data[i]['email'], user.email)

    def test_create_user_with_valid_data(self):
        client = APIClient()
        user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'ComplexPassword#123',
            're_password': 'ComplexPassword#123',
            'first_name': 'First',
            'last_name': 'Last',
            'position': Positions.CEO.value
        }
        response = client.post(reverse('register-user'), user_data, format='json')
        print(response.data)  # Вывод данных для диагностики
        self.assertEqual(response.status_code, 201)

    def test_create_user_with_invalid_data(self):
        client = APIClient()
        user_data = {'username': '', 'email': 'bademail'}
        response = client.post(reverse('register-user'), user_data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_create_user_with_missing_data(self):
        client = APIClient()
        user_data = {'username': 'missingemail'}
        response = client.post(reverse('register-user'), user_data, format='json')
        self.assertEqual(response.status_code, 400)