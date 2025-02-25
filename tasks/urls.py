from django.urls import path
from .views import CreateTaskView, GetAllTaskView

urlpatterns =[
    path("create-task/", CreateTaskView.as_view(), name="create-task"),
    path("get-tasks/", GetAllTaskView.as_view(), name="get-tasks")
]