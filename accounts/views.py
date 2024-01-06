from django.shortcuts import render
from django.db import transaction
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import LoginSerializer, RegistrationSerializer, MemberSerializer, PendingDataSerializer, OtpSerializer
from mainapp.models import Member
from mainapp.utils import otp_generator, email_sender, otp_expired
from accounts.models import Otp
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from accounts.models import PendingUserModel
from django.contrib.auth import get_user_model
# Create your views here.


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')
        if user is None:
            return Response({'detail': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user=user)

        return Response({'access_token': str(refresh.access_token),
                         'refresh_token': str(refresh)}, status=status.HTTP_200_OK)
                         

class RegistrationView(APIView):
    def post(self, request):

        serializer = PendingDataSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                try:
                    # handle otp sending generation and sending
                    otp_code = otp_generator.otp_generator()
                    email = serializer.validated_data['email']
                    username = serializer.validated_data['username']
                    otp_instance = Otp.objects.create(otp_code=otp_code, username=username)
                    otp_instance.save()
                    response = email_sender.sendEmail(
                        username=username, otp_code=otp_code, email=email)
                    if response:
                        instance = serializer.save()
                        return Response({'Detail': 'Otp code sent successfully'}, status=status.HTTP_200_OK)

                    raise Exception('Error sending Email')

                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OtpVerification(APIView):
    def post(self, request):
        serializer = OtpSerializer(data=request.data)
        if serializer.is_valid():
            otp_code = serializer.validated_data['otp_code']
            print(otp_code)
            try:
                with transaction.atomic():
                    try:
                        otp_instance = Otp.objects.get(otp_code=otp_code)
                        print(otp_instance.expire_at, otp_instance.otp_code)
                    except Otp.DoesNotExist:
                        return Response({'error': 'Invalid OTP code'}, status=status.HTTP_400_BAD_REQUEST)
                    if otp_expired.otp_expired(otp_timestamp=otp_instance.created_at):
                        otp_instance.delete()
                        return Response({'error': "Otp Expired"}, status=status.HTTP_400_BAD_REQUEST)

                    try:
                        pending_user = PendingUserModel.objects.get(
                            username=otp_instance.username)
                        print(pending_user.username)
                    except PendingUserModel.DoesNotExist:
                        return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

                    username = pending_user.username
                    email = pending_user.email
                    phone_number = pending_user.phone_number
                    print(username)
                    password = pending_user.password
                    date_of_birth = pending_user.date_of_birth

                    # user = get_user_model().objects.create(
                    #     username, email, phone_number, password, date_of_birth)
                    print(user)
                    user = RegistrationSerializer(data=pending_user)
                    if user.is_valid():
                        user.save(username=pending_user.username,
                                  email=pending_user.email, password=pending_user.password)
                    otp_instance.delete()

                    token = RefreshToken.for_user(user=user)
                    print(token)
                    return Response({"access": str(token.access_token),
                                    "refresh": token}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(APIView):
    authentication_classes = [JWTAuthentication]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query_set = Member.objects.all()
        serializer = MemberSerializer(query_set, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
