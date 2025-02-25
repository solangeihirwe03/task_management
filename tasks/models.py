from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tasks(models.Model):
    PRIORITY_CHOICES =[
        ("low","low"),
        ("medium", "medium"),
        ("high", "high")
    ]
    
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=512)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default="medium")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not User.objects.filter(id=self.assigned_to_id).exists():
            raise ValueError("Assigned user does not exist.")
        super().save(*args, **kwargs)

