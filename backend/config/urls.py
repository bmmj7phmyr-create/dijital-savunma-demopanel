from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Dijital Savunma API",
        default_version="v1",
        description="Dijital Savunma API Dokümantasyonu",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("", TemplateView.as_view(template_name="public.html"), name="public-page"),
    path("panel/", TemplateView.as_view(template_name="admin.html"), name="panel-page"),

    path("admin/", admin.site.urls),

    path("api/accounts/", include("accounts.api.urls")),
    path("api/members/", include("members.api.urls")),
    path("api/dashboard/", include("dashboard.api.urls")),
    path("api/applications/", include("applications.api.urls")),

    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]