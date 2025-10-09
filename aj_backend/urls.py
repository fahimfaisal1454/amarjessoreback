from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sitecontent.views import (
    BannerViewSet, AboutView, ProgramViewSet, ImpactStatViewSet,
    StoryViewSet, NewsViewSet, ContactCreateView
)
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r"banner", BannerViewSet, basename="banner")
router.register(r"programs", ProgramViewSet, basename="programs")   # keep old
router.register(r"projects", ProgramViewSet, basename="projects")   # NEW alias
router.register(r"impact", ImpactStatViewSet, basename="impact")
router.register(r"stories", StoryViewSet, basename="stories")
router.register(r"news", NewsViewSet, basename="news")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/about/", AboutView.as_view(), name="about"),
    path("api/contact/", ContactCreateView.as_view(), name="contact"),
     path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
