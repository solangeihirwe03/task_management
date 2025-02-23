from django.urls import path
from .views import TaskView

urlpatterns =[
    path("create-task/", TaskView.as_view(), name="create-task")
]