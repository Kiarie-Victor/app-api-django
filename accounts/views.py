from django.shortcuts import render
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import LoginSerializer

# Create your views here.

class LoginView(APIView):
    def post(self, request):
        print(request)
        serializer = LoginSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)

        user = serializer.context.get('user')
        if user is None:
            return Response({'detail': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user=user)

        return Response ({'access_token':str(refresh.access_token),
        'refresh_token':str(refresh)}, status=status.HTTP_200_OK)
       

