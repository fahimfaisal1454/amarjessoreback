from rest_framework import serializers
from .models import (
    BannerSlide, AboutSection, Program, ImpactStat, Story, News, ContactMessage
)

class BannerSlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerSlide
        fields = "__all__"

class BannerSlideAdminSerializer(serializers.ModelSerializer):
    # ensure proper coercion from multipart strings
    is_active = serializers.BooleanField(required=False)
    order = serializers.IntegerField(required=False)

    class Meta:
        model = BannerSlide
        fields = "__all__"

    def validate_cta_href(self, v):
        # Allow anchors (#about), relative (/news), or full URLs; reject spaces
        if v and " " in v:
            raise serializers.ValidationError("CTA link must not contain spaces")
        return v

class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutSection
        fields = ["badge_text", "heading", "highlight_words", "body", "points"]

class ProjectSerializer(serializers.ModelSerializer):
    """
    Public serializer for 'projects' (uses Program model behind the scenes).
    """
    class Meta:
        model = Program
        fields = ["id", "title", "slug", "summary", "icon", "image", "is_active", "order"]

class ProjectAdminSerializer(serializers.ModelSerializer):
    """
    Admin serializer for 'projects' CRUD (still Program model).
    """
    image = serializers.ImageField(required=False, allow_null=True)
    icon = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    slug = serializers.SlugField(required=False, allow_blank=True)

    class Meta:
        model = Program
        fields = ["id", "title", "slug", "summary", "icon", "image", "is_active", "order"]
        
        
class ImpactStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpactStat
        fields = "__all__"

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = "__all__"

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"
        read_only_fields = ["created_at"]
