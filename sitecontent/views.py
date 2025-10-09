from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    BannerSlide, AboutSection, Program, ImpactStat, Story, News, ContactMessage
)
from .serializers import (
    BannerSlideSerializer, AboutSerializer, ProgramSerializer, ImpactStatSerializer,
    StorySerializer, NewsSerializer, ContactMessageSerializer
)

# Home/Banner
class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BannerSlide.objects.filter(is_active=True).order_by("order", "id")
    serializer_class = BannerSlideSerializer
    permission_classes = [permissions.AllowAny]

# About (single)
class AboutView(APIView):
    def get(self, request):
        about = AboutSection.objects.order_by("-updated_at").first()
        if not about:
            return Response({
                "badge_text": "",
                "heading": "",
                "highlight_words": [],
                "body": "",
                "points": [],
            })
        return Response(AboutSerializer(about).data)

# Programs
class ProgramViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Program.objects.filter(is_active=True).order_by("order", "id")
    serializer_class = ProgramSerializer
    permission_classes = [permissions.AllowAny]

# Impact stats
class ImpactStatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ImpactStat.objects.all().order_by("order", "id")
    serializer_class = ImpactStatSerializer
    permission_classes = [permissions.AllowAny]

# Stories
class StoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Story.objects.filter(is_active=True).order_by("order", "id")
    serializer_class = StorySerializer
    permission_classes = [permissions.AllowAny]

# News (list + detail)
class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.filter(published=True)
    serializer_class = NewsSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

# Contact
class ContactCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]
