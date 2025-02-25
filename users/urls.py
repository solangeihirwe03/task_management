from django.urls import path
from .views import UserRegistrationView, UserLoginView, GetAllUserView


urlpatterns =[
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("get-users/", GetAllUserView.as_view(), name="get-users")
]