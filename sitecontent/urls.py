# project/urls.py  (replace the whole file with this)

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from sitecontent.views import (
    # Public
    BannerViewSet, AboutView, ProgramViewSet, ImpactStatViewSet,
    StoryViewSet, NewsViewSet, ContactCreateView, 
    # Admin
    BannerAdminViewSet,        ProgramAdminViewSet,
    AboutAdminView,            
)

# -------- Public API router (/api/...) --------
public_router = DefaultRouter()
public_router.register(r"banner", BannerViewSet, basename="banner")
public_router.register(r"programs", ProgramViewSet, basename="programs")
public_router.register(r"projects", ProgramViewSet, basename="projects")  # alias
public_router.register(r"impact", ImpactStatViewSet, basename="impact")
public_router.register(r"stories", StoryViewSet, basename="stories")
public_router.register(r"news", NewsViewSet, basename="news")

# -------- Admin API router (/api/admin/...) --------
admin_router = DefaultRouter()
admin_router.register(r"banners", BannerAdminViewSet, basename="admin-banners")
admin_router.register(r"programs", ProgramAdminViewSet, basename="admin-programs")

urlpatterns = [
    path("admin/", admin.site.urls),

    # --- ADMIN ROUTES FIRST (more specific) ---
    path("api/admin/", include(admin_router.urls)),
    path("api/admin/about/", AboutAdminView.as_view(), name="admin-about"),  # <-- this is the missing route

    # --- PUBLIC ROUTES AFTER (broader) ---
    path("api/", include(public_router.urls)),
    path("api/about/", AboutView.as_view(), name="about"),
    path("api/contact/", ContactCreateView.as_view(), name="contact"),

    # JWT auth
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh_alias"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
