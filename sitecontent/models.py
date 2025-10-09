from django.db import models
from django.utils.text import slugify

# 1) Banner/Hero (home)
class BannerSlide(models.Model):
    title = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="banner/")
    cta_text = models.CharField(max_length=60, blank=True)
    cta_href = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

# 2) About
class AboutSection(models.Model):
    badge_text = models.CharField(max_length=80, blank=True, default="")
    heading = models.CharField(max_length=200)
    highlight_words = models.JSONField(blank=True, null=True)
    body = models.TextField(blank=True, default="")
    points = models.JSONField(blank=True, null=True)   # <--- 3 bullets here
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading

# 3) Programs / Projects (grid)
class Program(models.Model):
    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    summary = models.TextField(blank=True)
    icon = models.CharField(max_length=60, blank=True)  # optional: lucide/shadcn icon name
    image = models.ImageField(upload_to="programs/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:150]
        return super().save(*args, **kwargs)

# 4) Impact stats (counters)
class ImpactStat(models.Model):
    label = models.CharField(max_length=120)   # e.g., "Volunteers", "Trees Planted"
    value = models.PositiveIntegerField()      # e.g., 250
    suffix = models.CharField(max_length=8, blank=True)  # e.g., "+"
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

# 5) Stories (short highlights or testimonials)
class Story(models.Model):
    title = models.CharField(max_length=160)
    excerpt = models.TextField(blank=True)
    image = models.ImageField(upload_to="stories/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

# 6) News (cards + detail optional)
class News(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    image = models.ImageField(upload_to="news/", blank=True, null=True)
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True)
    date = models.DateField()
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:190]
        return super().save(*args, **kwargs)

# 7) Contact messages (form POST)
class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    subject = models.CharField(max_length=160, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
