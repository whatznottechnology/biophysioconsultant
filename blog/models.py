from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.validators import URLValidator
import re


class BlogPost(models.Model):
    """
    Blog post model for YouTube health videos
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    CATEGORY_CHOICES = [
        ('physiotherapy', 'Physiotherapy'),
        ('acupressure', 'Acupressure'),
        ('massage', 'Massage Therapy'),
        ('nutrition', 'Nutrition'),
        ('exercise', 'Exercise & Fitness'),
        ('wellness', 'General Wellness'),
        ('alternative_medicine', 'Alternative Medicine'),
        ('mental_health', 'Mental Health'),
        ('pain_management', 'Pain Management'),
        ('rehabilitation', 'Rehabilitation'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200, help_text="Catchy title for the blog post")
    slug = models.SlugField(max_length=200, unique=True, help_text="URL-friendly version of title")
    
    # YouTube Video
    youtube_url = models.URLField(
        max_length=500,
        help_text="Full YouTube video URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID)"
    )
    youtube_video_id = models.CharField(
        max_length=20, 
        blank=True,
        help_text="YouTube video ID (automatically extracted from URL)"
    )
    
    # Content
    headline = models.CharField(
        max_length=300,
        help_text="Brief, engaging headline that summarizes the video content"
    )
    description = models.TextField(
        help_text="Detailed description of the video content and key takeaways"
    )
    key_points = models.TextField(
        blank=True,
        help_text="Bullet points of main topics covered (one per line)"
    )
    
    # Categorization
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='wellness'
    )
    tags = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated tags for better search (e.g., back pain, stretching, tips)"
    )
    
    # SEO and Meta
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="SEO meta description (recommended: 150-160 characters)"
    )
    
    # Status and Publishing
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Mark as featured to show on homepage"
    )
    
    # Analytics
    view_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status', 'published_at']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['is_featured', 'status']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Extract YouTube video ID from URL
        if self.youtube_url and not self.youtube_video_id:
            self.youtube_video_id = self.extract_youtube_id(self.youtube_url)
        
        # Set published_at when status changes to published
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        elif self.status != 'published':
            self.published_at = None
            
        # Auto-generate meta description if not provided
        if not self.meta_description and self.description:
            self.meta_description = self.description[:150] + "..." if len(self.description) > 150 else self.description
        
        super().save(*args, **kwargs)
    
    def extract_youtube_id(self, url):
        """Extract YouTube video ID from various YouTube URL formats"""
        patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([^&\n?#]+)',
            r'(?:https?://)?(?:www\.)?youtube\.com/embed/([^&\n?#]+)',
            r'(?:https?://)?(?:www\.)?youtu\.be/([^&\n?#]+)',
            r'(?:https?://)?(?:www\.)?youtube\.com/v/([^&\n?#]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return ''
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def get_youtube_embed_url(self):
        """Get YouTube embed URL for iframe"""
        if self.youtube_video_id:
            return f"https://www.youtube.com/embed/{self.youtube_video_id}?rel=0&modestbranding=1"
        return ""
    
    def get_youtube_thumbnail_url(self, quality='hqdefault'):
        """Get YouTube thumbnail URL"""
        if self.youtube_video_id:
            return f"https://img.youtube.com/vi/{self.youtube_video_id}/{quality}.jpg"
        return ""
    
    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []
    
    def get_key_points_list(self):
        """Return key points as a list"""
        if self.key_points:
            return [point.strip() for point in self.key_points.split('\n') if point.strip()]
        return []
    
    def increment_view_count(self):
        """Increment view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    @property
    def is_published(self):
        return self.status == 'published' and self.published_at
    
    @property
    def reading_time(self):
        """Estimate reading time based on description length"""
        word_count = len(self.description.split())
        # Average reading speed: 200 words per minute
        return max(1, round(word_count / 200))
