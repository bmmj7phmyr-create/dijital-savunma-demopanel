from django.urls import path
from .views import (
    ApplicationListCreateAPIView,
    ApplicationDetailAPIView,
    ApplicationApproveAPIView,
    ApplicationRejectAPIView,
)

urlpatterns = [
    path("", ApplicationListCreateAPIView.as_view(), name="application-list-create"),
    path("<int:pk>/", ApplicationDetailAPIView.as_view(), name="application-detail"),
    path("<int:pk>/approve/", ApplicationApproveAPIView.as_view(), name="application-approve"),
    path("<int:pk>/reject/", ApplicationRejectAPIView.as_view(), name="application-reject"),
]