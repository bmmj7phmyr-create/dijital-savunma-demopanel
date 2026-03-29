from django.urls import path
from .views import UserListAPIView, LoginAPIView, MeAPIView

urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="user-list"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("me/", MeAPIView.as_view(), name="me"),
]