from django.urls import path
from apps.users.views.user_views import *

urlpatterns = [
    path('', UserListGenericView.as_view(), name='users-list'),
    path('register/', RegisterUserGenericView.as_view(), name='register-user'),
]
