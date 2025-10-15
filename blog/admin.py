from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'status', 'is_featured', 
        'view_count', 'youtube_preview', 'published_at', 'created_at'
    ]
    list_filter = ['status', 'category', 'is_featured', 'created_at', 'published_at']
    search_fields = ['title', 'headline', 'description', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['youtube_video_id', 'view_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'headline', 'status', 'is_featured')
        }),
        ('YouTube Video', {
            'fields': ('youtube_url', 'youtube_video_id'),
            'description': 'YouTube video ID will be automatically extracted from the URL.'
        }),
        ('Content', {
            'fields': ('description', 'key_points'),
            'classes': ('wide',)
        }),
        ('Categorization', {
            'fields': ('category', 'tags'),
            'classes': ('collapse',)
        }),
        ('SEO & Meta', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
        ('Analytics & Timestamps', {
            'fields': ('view_count', 'published_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_published', 'make_draft', 'make_featured', 'remove_featured']
    
    def youtube_preview(self, obj):
        """Show YouTube thumbnail in admin"""
        if obj.youtube_video_id:
            thumbnail_url = obj.get_youtube_thumbnail_url('default')
            return format_html(
                '<img src="{}" width="60" height="45" style="border-radius: 4px;" />',
                thumbnail_url
            )
        return "No video"
    youtube_preview.short_description = "Preview"
    
    def make_published(self, request, queryset):
        """Bulk action to publish posts"""
        updated = queryset.update(status='published')
        self.message_user(request, f'{updated} posts were marked as published.')
    make_published.short_description = "Mark selected posts as published"
    
    def make_draft(self, request, queryset):
        """Bulk action to make posts draft"""
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} posts were marked as draft.')
    make_draft.short_description = "Mark selected posts as draft"
    
    def make_featured(self, request, queryset):
        """Bulk action to make posts featured"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} posts were marked as featured.')
    make_featured.short_description = "Mark selected posts as featured"
    
    def remove_featured(self, request, queryset):
        """Bulk action to remove featured status"""
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} posts were unmarked as featured.')
    remove_featured.short_description = "Remove featured status"
