from .serializers import TaskSerizalizers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class TaskView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer = TaskSerizalizers(data=request.data)
        
        if serializer.is_valid():
            task = serializer.save()
            task_data = TaskSerizalizers(task).data
            return Response(
                {
                "message": "Task created successfully!",
                "task": task_data
                },
                status= status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
