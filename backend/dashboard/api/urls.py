from django.urls import path
from .views import DashboardAPIView, BackupAPIView

urlpatterns = [
    path("", DashboardAPIView.as_view(), name="dashboard"),
    path("backup/", BackupAPIView.as_view(), name="backup"),
]