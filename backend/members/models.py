from django.db import models


class Member(models.Model):
    STATUS_CHOICES = (
        ("active", "Aktif"),
        ("inactive", "Pasif"),
        ("pending", "Başvuru"),
    )

    ROLE_CHOICES = (
        ("member", "Üye"),
        ("board", "Yönetim"),
        ("admin", "Admin"),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, default="")
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    tcno = models.CharField(max_length=11, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profession = models.CharField(max_length=150, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")

    dues_status = models.CharField(max_length=30, blank=True, null=True, default="Bekliyor")
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    joined_at = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()