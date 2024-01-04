from rest_framework import serializers
from mainapp.models import Member
from accounts.models import PendingUserModel, Otp
import re
import phonenumbers
from django.contrib.auth import authenticate,login
from django.contrib.auth import get_user_model

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ("username", "email", "phone_number", "password", "date_of_birth")

    def validate_username(self, username:str) -> str:
        if not username.strip():
            serializers.ValidationError('Username cannot be empty')

        existing__users = Member.objects.filter(username=username)

        if existing__users.exists():
            raise serializers.ValidationError('This Username is already taken')

        return username
    def validate_email(self, email: str) -> str:
        if not email.strip():
            raise serializers.ValidationError('Email Field cannot be empty')

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise serializers.ValidationError('Invalid Email format')

        existing_email = Member.objects.filter(email=email)
        if existing_email.exists():
            serializers.ValidationError('The email is already taken')
        return email

    def validate_phone_number(self, phone_number:str):
        if not phone_number.strip():
            raise serializers.ValidationError('Phone_number cannot be empty.')

        try:
            parsed_number = phonenumbers.parse(phone_number, region='KE')
            if not phonenumbers.is_valid_number(parsed_number):
                raise serializers.ValidationError('Invalid number format')
            else:
                phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        except:
            raise serializers.ValidationError('Invalid number format')

        return phone_number

    def validate_password(self, password:str):
        if not password.strip():
            raise serializers.ValidationError('Password cannot be empty')

        if not any( char.isupper() for char in password):
            raise serializers.ValidationError('Password must contain at least one uppercase letter')

        if not any( char.isdigit() for char in password):
            raise serializers.ValidationError('Password must contain at least one digit')

        if not any( (char in "!@#$%^&*()-_=+[]|;:'\",.<>?/") for char in password):
            raise serializers.ValidationError("Password must contain at least one of the following special characters: !@#$%^&*()-_=+[]|;:'\",.<>?/")
            
        return password

    def validate_date_of_birth(self, date_of_birth:str):
        dob = str(date_of_birth)
        if not dob.strip():
            serializers.ValidationError('The date of birth cannot be empty my guy')

        return date_of_birth

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data:dict):
        email = data.get('email')
        password = data.get('password')
        request = self.context.get('request')

        user = authenticate(request=request, email = email, password = password)

        if not user :
            raise serializers.ValidationError('Invalid login credentials')

        login(request=request,user=user)

        #assigning user to data dictionary in oder to use give the user tokens
        data['user'] = user

        return data

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ("username", "email", "phone_number", "date_of_birth")

class PendingDataSerializer( serializers.ModelSerializer):
    class Meta:
        model =  PendingUserModel
        fields = ('username', 'email', 'phone_number', 'password', 'date_of_birth')

class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ('otp_code',)