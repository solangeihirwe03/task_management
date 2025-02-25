from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["id","email", "password"]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return User.objects.create(**validated_data)
    

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")
        
        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password. please try again.")
        
        data["user"] = user

        return data
    
class GetAllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]
        
    def to_representation(self, instance):
        """Convert instance into JSON serializableformat"""
        data = super().to_representation(instance)
        return data
        