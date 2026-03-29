from rest_framework import serializers
from members.models import Member


class MemberSerializer(serializers.ModelSerializer):
    ad           = serializers.CharField(write_only=False, required=False, allow_blank=True)
    telefon      = serializers.CharField(source="phone", required=False, allow_blank=True, allow_null=True)
    dogumTarihi  = serializers.DateField(source="birth_date", required=False, allow_null=True)
    meslek       = serializers.CharField(source="profession", required=False, allow_blank=True, allow_null=True)
    adres        = serializers.CharField(source="address", required=False, allow_blank=True, allow_null=True)
    durum        = serializers.CharField(required=False, allow_blank=True)
    rol          = serializers.CharField(required=False, allow_blank=True)
    aidat        = serializers.CharField(source="dues_status", required=False, allow_blank=True, allow_null=True)
    borc         = serializers.DecimalField(source="debt", max_digits=10, decimal_places=2, required=False)
    giris        = serializers.DateField(source="joined_at", required=False, allow_null=True)

    class Meta:
        model = Member
        fields = [
            "id", "ad", "email", "telefon", "tcno",
            "dogumTarihi", "meslek", "adres", "durum",
            "rol", "aidat", "borc", "giris",
        ]
        extra_kwargs = {
            "email": {"required": True},
        }

    def _split_name(self, full_name):
        parts = (full_name or "").strip().split()
        if not parts:
            return "", ""
        return parts[0], " ".join(parts[1:]) if len(parts) > 1 else ""

    def _map_status(self, value):
        return {
            "Aktif": "active", "Pasif": "inactive", "Başvuru": "pending",
            "active": "active", "inactive": "inactive", "pending": "pending",
        }.get(value, "active")

    def _map_role(self, value):
        return {
            "Üye": "member", "Yönetim": "board", "Admin": "admin",
            "Gönüllü": "member", "Aday": "member",
            "member": "member", "board": "board", "admin": "admin",
        }.get(value, "member")

    def create(self, validated_data):
        ad    = validated_data.pop("ad", "")
        durum = validated_data.pop("durum", "Aktif")
        rol   = validated_data.pop("rol", "Üye")

        first_name, last_name = self._split_name(ad)
        validated_data["first_name"] = first_name
        validated_data["last_name"]  = last_name
        validated_data["status"]     = self._map_status(durum)
        validated_data["role"]       = self._map_role(rol)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        ad    = validated_data.pop("ad", None)
        durum = validated_data.pop("durum", None)
        rol   = validated_data.pop("rol", None)

        if ad:
            instance.first_name, instance.last_name = self._split_name(ad)
        if durum:
            instance.status = self._map_status(durum)
        if rol:
            instance.role = self._map_role(rol)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance

    def to_representation(self, instance):
        return {
            "id":          instance.id,
            "ad":          instance.full_name,
            "email":       instance.email,
            "telefon":     instance.phone or "",
            "tcno":        instance.tcno or "",
            "dogumTarihi": str(instance.birth_date) if instance.birth_date else "",
            "meslek":      instance.profession or "",
            "adres":       instance.address or "",
            "durum": {
                "active": "Aktif", "inactive": "Pasif", "pending": "Başvuru",
            }.get(instance.status, instance.status),
            "rol": {
                "member": "Üye", "board": "Yönetim", "admin": "Admin",
            }.get(instance.role, instance.role),
            "aidat": instance.dues_status or "Bekliyor",
            "borc":  str(instance.debt),
            "giris": str(instance.joined_at) if instance.joined_at else "",
        }