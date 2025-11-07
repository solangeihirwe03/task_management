from rest_framework import serializers
from .models import Tasks
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateTaskSerizalizers(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all())
    class Meta:
        model = Tasks
        fields = "__all__"
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
        extra_kwargs = {
            "title": {"required": True},
            "description": {"required": True},
            "assigned_to": {"required": True},
        }
        
    def validate_assigned_to(self, value):
        """Check if assigned user exists in the database."""
        if not value or not value.id:
            raise serializers.ValidationError("Assigned user doesn't exists.")
        return value
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.email)
        
        
    def create(self, validated_data):
        """Create a new task"""
        user = self.context['request'].user  # Get the current authenticated user
        validated_data['created_by'] = user  # Assign the current user to 'created_by'
        return Tasks.objects.create(**validated_data)
    
class GetTasksSerializer(serializers.ModelSerializer):
    assigned_to_email = serializers.EmailField(source="assigned_to.email", read_only=True)
    
    class Meta:
        model = Tasks
        fields = ["id", "title", "description", "assigned_to_email", "priority", "created_by", "created_at", "updated_at"]
        
class UpdateTaskSerializer(serializers.ModelSerializer):
    assigned_to_email = serializers.EmailField(source="assigned_to.email", read_only=True)
    created_by_email = serializers.EmailField(source="created_by.email", read_only=True)
    class Meta:
        model = Tasks
        fields = ["id","title", "description", "assigned_to_email", "priority", "created_by_email", "created_at", "updated_at"]
        extra_kwargs = {
            "title": {"required": False},
            "description": {"required": False},
            "assigned_to": {"required": False},
            "priority": {"required": False},
        }
        
    def update(self, instance, validated_data):
        """Update task only the provided field"""
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        instance.refresh_from_db()
        return instance
        
        