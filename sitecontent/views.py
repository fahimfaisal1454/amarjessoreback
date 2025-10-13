from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from .models import (
    BannerSlide, AboutSection, Program, ImpactStat, Story, News, ContactMessage
)
from .serializers import (
    BannerSlideSerializer, AboutSerializer,  ImpactStatSerializer,
    StorySerializer, NewsSerializer, ContactMessageSerializer, BannerSlideAdminSerializer,  ProjectSerializer, ProjectAdminSerializer
)

# Home/Banner
class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BannerSlide.objects.filter(is_active=True).order_by("order", "id")
    serializer_class = BannerSlideSerializer
    permission_classes = [permissions.AllowAny]

class BannerAdminViewSet(viewsets.ModelViewSet):
    """
    /api/admin/banners/  -> list, create
    /api/admin/banners/{id}/ -> retrieve, update/partial_update, delete
    """
    queryset = BannerSlide.objects.all().order_by("order", "id")
    serializer_class = BannerSlideAdminSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]    

# About (single)
class AboutView(APIView):
    permission_classes = [permissions.AllowAny]
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


class AboutAdminView(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def _get(self):
        obj, _ = AboutSection.objects.get_or_create(
            pk=1,
            defaults={"badge_text": "", "heading": "", "highlight_words": [], "body": "", "points": []},
        )
        return obj

    def get(self, request):
        return Response(AboutSerializer(self._get()).data)

    def put(self, request):
        about = self._get()
        data = request.data.copy()

        to_list = lambda v, sep: v if isinstance(v, list) else (
            [s for s in map(str.strip, (json.loads(v) if isinstance(v, str) and v.strip().startswith("[") else v.split(sep))) if s]
            if isinstance(v, str) else []
        )

        data["highlight_words"] = to_list(data.get("highlight_words", []), ",")
        data["points"] = to_list(data.get("points", []), "\n")

        ser = AboutSerializer(about, data=data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_200_OK)
# Programs
class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
  """
  Public list of projects (backed by Program table).
  """
  queryset = Program.objects.filter(is_active=True).order_by("order", "id")
  serializer_class = ProjectSerializer
  permission_classes = [permissions.AllowAny]


class ProjectAdminViewSet(viewsets.ModelViewSet):
  """
  /api/admin/projects/  -> CRUD for dashboard
  """
  queryset = Program.objects.all().order_by("order", "id")  # still using Program model
  serializer_class = ProjectAdminSerializer
  permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
  parser_classes = [MultiPartParser, FormParser, JSONParser]
    
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
