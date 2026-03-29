from django.db import models


class Application(models.Model):
    STATUS_CHOICES = (
        ("pending", "Bekliyor"),
        ("approved", "Onaylandı"),
        ("rejected", "Reddedildi"),
    )

    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100, blank=True, default="")
    email      = models.EmailField(unique=True)
    phone      = models.CharField(max_length=20, blank=True, null=True)
    tcno       = models.CharField(max_length=11, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profession = models.CharField(max_length=150, blank=True, null=True)
    city       = models.CharField(max_length=100, blank=True, null=True)
    address    = models.TextField(blank=True, null=True)
    specialty  = models.CharField(max_length=150, blank=True, null=True)
    note       = models.TextField(blank=True, null=True)
    contact_permission = models.BooleanField(default=False)
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.status}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
