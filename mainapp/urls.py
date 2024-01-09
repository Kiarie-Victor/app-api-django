from django.urls import path
from .views import UsersView


urlpatterns = [
    path('api/users/', UsersView.as_view(), name='users'),
]
