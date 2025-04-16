from .serializers import CreateTaskSerizalizers, GetTasksSerializer, UpdateTaskSerializer
from .models import Tasks
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404

class CreateTaskView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        request.data['created_by'] = request.user.email
        serializer = CreateTaskSerizalizers(data=request.data, context={"request": request})
        if serializer.is_valid():
            task = serializer.save()
            task_data = CreateTaskSerizalizers(task).data
            return Response(
                {
                "message": "Task created successfully!",
                "task": task_data
                },
                status= status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetAllTaskView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        tasks = Tasks.objects.all()
        
        if not tasks.exists():
            return Response(
                {
                "status": status.HTTP_404_NOT_FOUND,
                "message": "No tasks found"
                },
                status=status.HTTP_404_NOT_FOUND)
            
        serializer = GetTasksSerializer(tasks, many=True)
        return Response(
            {
                "status": status.HTTP_200_OK,
                "data": serializer.data
            },
            status= status.HTTP_200_OK
        )
        
class GetTaskByIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, task_id, *args, **kwargs):
        task = Tasks.objects.get(id=task_id)
        serializer = GetTasksSerializer(task)
        return Response(
            {
                "message": "Task found successfully!",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
   
class UpdateTaskBYIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]    
    
    def put(self, request, task_id, *args, **kwargs):
        """Allow partial update of task"""
        
        try:
            task = Tasks.objects.get(id=task_id)
        except Tasks.DoesNotExist:
            return Response(
                {
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Task not found"
                },
                status=status.HTTP_404_NOT_FOUND)
        
        if task.created_by != request.user:
            return Response(
                {
                    "status": status.HTTP_403_FORBIDDEN,
                    "message": "You are not the creator of this task, so you cannot delete it."
                },
                status=status.HTTP_403_FORBIDDEN
            )  
            
        serializer = UpdateTaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Task updated successfully!", 
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteTaskByIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, task_id):
        """Delete a task by id"""
        
        try:
            task = Tasks.objects.get(id=task_id)
            
        except Tasks.DoesNotExist:
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Task not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        if task.created_by != request.user:
            return Response(
                {
                    "status": status.HTTP_403_FORBIDDEN,
                    "message": "You are not the creator of this task, so you cannot delete it."
                },
                status=status.HTTP_403_FORBIDDEN
            )   
        task.delete()
        return Response(
            {
                "message": "Task deleted successfully!"
            },
            status=status.HTTP_204_NO_CONTENT
        )