from django.db import models
from mainapp.models import Member
from django.utils import timezone

# Create your models here.
class Otp(models.Model):
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

class PendingUserModel(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=20)
    date_of_birth = models.DateTimeField(default=(timezone.now() + timezone.timedelta(minutes=3)))