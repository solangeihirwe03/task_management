from .serializers import CreateTaskSerizalizers, GetTasksSerializer
from .models import Tasks
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class CreateTaskView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer = CreateTaskSerizalizers(data=request.data)
        
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
