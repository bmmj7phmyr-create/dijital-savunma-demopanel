from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.models import Application
from members.models import Member
from .serializers import ApplicationSerializer


class ApplicationListCreateAPIView(APIView):

    def get_permissions(self):
        # GET → sadece admin (token gerekli)
        # POST → herkese açık (public.html başvuru formu)
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        applications = Application.objects.all().order_by("-id")
        serializer = ApplicationSerializer(applications, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        # "not" Python keyword olduğu için data kopyasını düzenliyoruz
        data = request.data.copy() if hasattr(request.data, "copy") else dict(request.data)

        serializer = ApplicationSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return Application.objects.get(pk=pk)

    def get(self, request, pk):
        application = self.get_object(pk)
        serializer = ApplicationSerializer(application, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        application = self.get_object(pk)
        serializer = ApplicationSerializer(application, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        application = self.get_object(pk)
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApplicationApproveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            application = Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            return Response({"detail": "Başvuru bulunamadı."}, status=status.HTTP_404_NOT_FOUND)

        if application.status == "approved":
            return Response(
                {"detail": "Bu başvuru zaten onaylandı."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Member.objects.filter(email=application.email).exists():
            return Response(
                {"detail": "Bu e-posta adresiyle kayıtlı üye zaten mevcut."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Member.objects.create(
            first_name=application.first_name,
            last_name=application.last_name,
            email=application.email,
            phone=application.phone,
            tcno=application.tcno,
            birth_date=application.birth_date,
            profession=application.profession,
            address=application.address,
            status="active",
            role="member",
            dues_status="Bekliyor",
            debt=1200,
        )

        application.status = "approved"
        application.save()

        return Response(
            {"detail": "Başvuru onaylandı, üye kaydı oluşturuldu."},
            status=status.HTTP_200_OK,
        )


class ApplicationRejectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            application = Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            return Response({"detail": "Başvuru bulunamadı."}, status=status.HTTP_404_NOT_FOUND)

        if application.status == "rejected":
            return Response(
                {"detail": "Bu başvuru zaten reddedildi."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        application.status = "rejected"
        application.save()

        return Response(
            {"detail": "Başvuru reddedildi."},
            status=status.HTTP_200_OK,
        )