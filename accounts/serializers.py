from rest_framework import serializers
from mainapp.models import Member
from accounts.models import PendingUserModel, Otp
import re
import phonenumbers
from django.contrib.auth import authenticate, login, get_user_model

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ("username", "email", "phone_number", "password", "date_of_birth")

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

class PendingDataSerializer( serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    password = serializers.CharField()
    date_of_birth = serializers.CharField()


    def validate_username(self, username:str):
        if not username.strip():
            raise serializers.ValidationError('Username cannot be empty.')
        if Member.objects.filter(username=username).exists():
            raise serializers.ValidationError('This username is already taken.')

        return username

    def validate_email(self, email):
        if not email.strip():
            raise serializers.ValidationError('Email cannot be empty.')

        reg_ex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$'
        if not re.match(reg_ex, email):
            raise serializers.ValidationError('Invalid Email format.')

        if Member.objects.filter(email=email).exists():
            raise serializers.ValidationError('The email is already taken.')

        return email

    def validate_phone_number(self, phone_number:str):
        if not phone_number.strip():
            raise serializers.ValidationError('Phone Number field cannot be empty')
        try:
            parsed_number = phonenumbers.parse(phone_number, region='KE')
            if not phonenumbers.is_valid_number(parsed_number):
                raise serializers.ValidationError('Invalid phone number format')
            else:
                phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError('Invalid phone number format')

        return phone_number

    def validate_password(self, password:str):
        if not password.strip():
            raise serializers.ValidationError('Password cannot be empty')

        if not any( char.isupper() for char in password):
            raise  serializers.ValidationError('Password must contain at least one uppercase letter')

        if not any( char.isdigit() for char in password):
            raise serializers.ValidationError('Password must contain at least one digit.')

        if (len(password) < 8):
            raise serializers.ValidationError("Password must not be less than 8 digits.")

        if not any( (char in "!@#$%^&*()-_=+[]|;:'\",.<>?/") for char in password):
            raise serializers.ValidationError("Password must contain at least one of the following special characters: !@#$%^&*()-_=+[]|;:'\",.<>?/")

        return password
    
    def validate_date_of_birth(self, date_of_birth:str):
        if not date_of_birth.strip():
            raise  serializers.ValidationError('Date of birth field cannot be empty')

        return date_of_birth

class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ('otp_code',)

        def validate_otp_code(self, otp:str):
            stripped_otp = otp.strip()
            if len(stripped_otp) == 6:
                serializers.ValidationError('Invalid OTP code.')

            return stripped_otp