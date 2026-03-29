from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import User
from accounts.permissions import IsAdminUserCustom
from .serializers import UserSerializer


class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserCustom]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class LoginAPIView(TokenObtainPairView):
    pass


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)