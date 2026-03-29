from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("staff", "Staff"),
        ("manager", "Manager"),
    )

    full_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="staff")

    def __str__(self):
        return self.username
    from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("staff", "Staff"),
        ("manager", "Manager"),
    )

    full_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="staff")

    def __str__(self):
        return self.username


class Transaction(models.Model):
    TYPE_CHOICES = (
        ("income", "Gelir"),
        ("expense", "Gider"),
    )

    CATEGORY_CHOICES = (
        ("aidat", "Aidat"),
        ("bagis", "Bağış"),
        ("gider", "Gider"),
        ("diger", "Diğer"),
    )

    CHANNEL_CHOICES = (
        ("kasa", "Kasa"),
        ("banka", "Banka"),
        ("diger", "Diğer"),
    )

    code = models.CharField(max_length=30, unique=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="diger")
    description = models.TextField(blank=True, null=True)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default="banka")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.type} - {self.amount}"
