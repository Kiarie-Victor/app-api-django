from rest_framework import serializers
from .models import Member

class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('username', 'email', 'phone_number', 'password', 'date_of_birth')
