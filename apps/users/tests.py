from django.test import TestCase
import pytest
from apps.users.models import User
from unittest.mock import patch
from apps.users.serializers import UserSerializer
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.fixture
def user_fixture(db):
    user1 = User.objects.create(username='testuser1', email='test1@example.com')
    user2 = User.objects.create(username='testuser2', email='test2@example.com')
    return [user1, user2]

def test_get_all_users(user_fixture):
    client = APIClient()
    response = client.get(reverse('users-list'))
    assert response.status_code == 200
    assert len(response.data) == len(user_fixture)

def test_get_users_by_project_name(user_fixture):
    client = APIClient()
    project_name = 'example_project'
    response = client.get(reverse('users-list'), {'project': project_name})
    assert response.status_code == 200

def test_get_empty_users_list():
    client = APIClient()
    with patch('apps.users.models.User.objects.all', return_value=[]):
        response = client.get(reverse('users-list'))
        assert response.status_code == 200
        assert response.data == []

def test_user_serializer(user_fixture):
    serialized_data = UserSerializer(user_fixture, many=True).data
    for i, user in enumerate(user_fixture):
        assert serialized_data[i]['username'] == user.username
        assert serialized_data[i]['email'] == user.email

def test_create_user_with_valid_data():
    client = APIClient()
    user_data = {'username': 'newuser', 'email': 'newuser@example.com'}
    response = client.post(reverse('users-list'), user_data, format='json')
    assert response.status_code == 201

def test_create_user_with_invalid_data():
    client = APIClient()
    user_data = {'username': '', 'email': 'bademail'}
    response = client.post(reverse('users-list'), user_data, format='json')
    assert response.status_code == 400

def test_create_user_with_missing_data():
    client = APIClient()
    user_data = {'username': 'missingemail'}
    response = client.post(reverse('users-list'), user_data, format='json')
    assert response.status_code == 400