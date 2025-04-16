from django.urls import path
from .views import CreateTaskView, GetAllTaskView, GetTaskByIdView, UpdateTaskBYIdView, DeleteTaskByIdView

urlpatterns =[
    path("create-task/", CreateTaskView.as_view(), name="create-task"),
    path("get-tasks/", GetAllTaskView.as_view(), name="get-tasks"),
    path("get-task/<int:task_id>/", GetTaskByIdView.as_view(), name="get-task-by-id" ),
    path("update-task/<int:task_id>/", UpdateTaskBYIdView.as_view(), name="update-task"),
    path("delete-task/<int:task_id>", DeleteTaskByIdView.as_view(), name="delete-task")
]