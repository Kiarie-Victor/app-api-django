from django.db import models
from mainapp.utils.uuid_abstract import UUIDGenerator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import phonenumbers
# Create your models here.
class MemberManager(BaseUserManager):
    def create_user(self, email, username, phone_number,date_of_birth, password,**extra_fields):
        if not email:
            raise ValueError(_('The Email field must eb set'))

        normalized_email = self.normalize_email(email)

        try:
            parsed_number = phonenumbers.parse(phone_number, region = 'KE')
            if not phonenumbers.is_valid_number(parsed_number):
                ValueError('Invalid Phone Number Input')
            else:
                phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        except:
            raise ValueError('Invalid Number Format')

            date_of_birth = date_of_birth.strftime('%Y-%m-%d')

        user = self.model(
            email = normalized_email,
            username = username , 
            phone_number = phone_number,
            date_of_birth = date_of_birth,
            **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self,email,username ,phone_number, date_of_birth, password = None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(email,username,  phone_number, date_of_birth , password,**extra_fields)

class Member (AbstractBaseUser, PermissionsMixin, UUIDGenerator, models.Model):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, max_length=50)
    phone_number = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=100)
    date_of_birth = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = MemberManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','phone_number','date_of_birth']

    def __str__(self):
        return f"{self.username}"
    

