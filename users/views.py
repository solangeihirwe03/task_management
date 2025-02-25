from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, GetAllUsersSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication


User = get_user_model()


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user_data = UserRegistrationSerializer(user).data
            return Response(
                {
                    "message": "User registered successfully!",
                    "user": user_data 
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Logged in successfully!",
                "token": token.key
            },
            status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class GetAllUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes= [IsAuthenticated]
    
    def get(self, request):
        users = User.objects.all()
        if not users.exists():
            return Response(
            {
            "status": status.HTTP_404_NOT_FOUND,
            "message": "Users not found"
            },
            status=status.HTTP_404_NOT_FOUND)
        serializer = GetAllUsersSerializer(users, many=True)
        return Response(
        {
            "message": "Users found successfully!" ,
            "data": serializer.data
        }, 
        status=status.HTTP_200_OK)