from django.db import models
from mainapp.models import Member
from datetime import timezone
from django.utils import timezone

# Create your models here.
class Otp(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now())
    is_verified = models.BooleanField(default=False)