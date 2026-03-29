from django.urls import path
from .views import MemberListCreateAPIView, MemberDetailAPIView

urlpatterns = [
    path("", MemberListCreateAPIView.as_view(), name="member-list-create"),
    path("<int:pk>/", MemberDetailAPIView.as_view(), name="member-detail"),
]