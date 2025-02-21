from rest_framework import serializers
from .models import Tasks
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskSerizalizer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = "__all__"
        extra_kwargs = {
            "title": {"required": True},
            "description": {"required": True},
            "assigned_to": {"required": True},
            "priority": {"required": True}
        }
        
    def validate_assigned_to(self, value):
        """Check if assigned user exists in the database."""
        if not value or not value.id:
            raise serializers.ValidationError("Assigned user doesn't exists.")
        return value
    
    def create(self, validated_data):
        """Create a new task"""
        return Tasks.objects.create(**validated_data)