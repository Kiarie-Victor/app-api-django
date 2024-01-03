from django.shortcuts import render
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import LoginSerializer, RegistrationSerializer
from mainapp.models import Member

# Create your views here.

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')
        if user is None:
            return Response({'detail': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user=user)

        return Response ({'access_token':str(refresh.access_token),
        'refresh_token':str(refresh)}, status=status.HTTP_200_OK)
    
class RegistrationView(APIView):
    def post(self, request):

        serializer = RegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user=user)
            return Response ({'access_token':str(refresh.access_token),
            'refresh_token':str(refresh)})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


