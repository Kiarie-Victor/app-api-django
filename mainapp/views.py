from django.shortcuts import render
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from mainapp.models import Member
from mainapp.serializers import UsersListSerializer

# Create your views here.

class UsersView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request):
        try:
            query_set = Member.objects.all()
            serializer = UsersListSerializer(query_set, many = True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Member.DoesNotExist:
            return Response({"details" : "There was an error retrieving data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR )
            
        

