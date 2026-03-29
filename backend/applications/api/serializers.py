from rest_framework import serializers
from applications.models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    # HTML'den gelen Türkçe field isimleri → model field'larına eşleme
    ad            = serializers.CharField(write_only=True, required=True)
    dogumTarihi   = serializers.DateField(source="birth_date", required=False, allow_null=True)
    meslek        = serializers.CharField(source="profession", required=False, allow_blank=True, allow_null=True)
    sehir         = serializers.CharField(source="city", required=False, allow_blank=True, allow_null=True)
    adres         = serializers.CharField(source="address", required=False, allow_blank=True, allow_null=True)
    uzmanlik      = serializers.CharField(source="specialty", required=False, allow_blank=True, allow_null=True)
    telefon       = serializers.CharField(source="phone", required=False, allow_blank=True, allow_null=True)
    iletisimIzni  = serializers.BooleanField(source="contact_permission", required=False, default=False)
    durum         = serializers.SerializerMethodField()
    tarih         = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            "id",
            "ad",
            "email",
            "telefon",
            "tcno",
            "dogumTarihi",
            "meslek",
            "sehir",
            "adres",
            "uzmanlik",
            "iletisimIzni",
            "status",
            "durum",
            "tarih",
            "created_at",
        ]
        # not alanı Python keyword'ü olduğu için özel işlem
        extra_kwargs = {
            "status": {"read_only": True},
        }

    def get_durum(self, obj):
        mapping = {
            "pending":  "Bekliyor",
            "approved": "Onaylandı",
            "rejected": "Reddedildi",
        }
        return mapping.get(obj.status, obj.status)

    def get_tarih(self, obj):
        if obj.created_at:
            return obj.created_at.strftime("%Y-%m-%d")
        return None

    def _split_name(self, full_name):
        parts = (full_name or "").strip().split()
        if not parts:
            return "", ""
        if len(parts) == 1:
            return parts[0], ""
        return parts[0], " ".join(parts[1:])

    def validate(self, attrs):
        # "not" field'ı Python keyword'ü — form'dan "not" key'i olarak gelir
        request = self.context.get("request")
        if request and "not" in request.data:
            attrs["note"] = request.data["not"]
        return attrs

    def create(self, validated_data):
        ad = validated_data.pop("ad")
        first_name, last_name = self._split_name(ad)
        validated_data["first_name"] = first_name
        validated_data["last_name"]  = last_name
        return super().create(validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # HTML panelin beklediği tüm alanlar
        data["id"]           = instance.id
        data["ad"]           = instance.full_name
        data["email"]        = instance.email
        data["telefon"]      = instance.phone or ""
        data["tcno"]         = instance.tcno or ""
        data["dogumTarihi"]  = str(instance.birth_date) if instance.birth_date else ""
        data["meslek"]       = instance.profession or ""
        data["sehir"]        = instance.city or ""
        data["adres"]        = instance.address or ""
        data["uzmanlik"]     = instance.specialty or ""
        data["not"]          = instance.note or ""
        data["iletisimIzni"] = instance.contact_permission
        data["tarih"]        = instance.created_at.strftime("%Y-%m-%d") if instance.created_at else ""
        data["durum"]        = {
            "pending":  "Bekliyor",
            "approved": "Onaylandı",
            "rejected": "Reddedildi",
        }.get(instance.status, instance.status)
        return data