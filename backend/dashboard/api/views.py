import os
import subprocess
from datetime import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from members.models import Member
from applications.models import Application


class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_members = Member.objects.count()
        total_applications = Application.objects.count()
        pending_applications = Application.objects.filter(status="pending").count()
        approved_applications = Application.objects.filter(status="approved").count()
        rejected_applications = Application.objects.filter(status="rejected").count()

        return Response({
            "total_members": total_members,
            "total_applications": total_applications,
            "pending_applications": pending_applications,
            "approved_applications": approved_applications,
            "rejected_applications": rejected_applications,
        })


class BackupAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        db_name = os.getenv("POSTGRES_DB")
        db_user = os.getenv("POSTGRES_USER")
        db_password = os.getenv("POSTGRES_PASSWORD")
        db_host = "db"
        db_port = "5432"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = "/app/backups"
        os.makedirs(backup_dir, exist_ok=True)
        backup_file = f"{backup_dir}/yedek_{timestamp}.sql"

        env = os.environ.copy()
        env["PGPASSWORD"] = db_password or ""

        try:
            result = subprocess.run(
                [
                    "pg_dump",
                    "-h", db_host,
                    "-p", db_port,
                    "-U", db_user,
                    "-d", db_name,
                    "-f", backup_file,
                ],
                env=env,
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode != 0:
                return Response(
                    {"detail": f"Yedekleme başarısız: {result.stderr}"},
                    status=500,
                )

            file_size = os.path.getsize(backup_file)
            return Response({
                "detail": "Yedekleme başarıyla tamamlandı.",
                "file": f"yedek_{timestamp}.sql",
                "size_kb": round(file_size / 1024, 1),
                "timestamp": timestamp,
            })

        except subprocess.TimeoutExpired:
            return Response({"detail": "Yedekleme zaman aşımına uğradı."}, status=500)
        except FileNotFoundError:
            return Response({"detail": "pg_dump bulunamadı. postgresql-client kurulu değil."}, status=500)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)