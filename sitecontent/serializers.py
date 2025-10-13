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

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = "__all__"

class ProgramAdminSerializer(serializers.ModelSerializer):
    # ensure coercion when coming from multipart/form-data
    is_active = serializers.BooleanField(required=False)
    order = serializers.IntegerField(required=False, min_value=0)

    class Meta:
        model = Program
        fields = "__all__"
        
        
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
