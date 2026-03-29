from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from members.models import Member
from .serializers import MemberSerializer


class MemberListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        members = Member.objects.all().order_by("-id")
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return Member.objects.get(pk=pk)

    def get(self, request, pk):
        member = self.get_object(pk)
        serializer = MemberSerializer(member)
        return Response(serializer.data)

    def put(self, request, pk):
        member = self.get_object(pk)
        serializer = MemberSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        member = self.get_object(pk)
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)