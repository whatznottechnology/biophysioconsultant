from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(ModelAdmin):
    list_display = [
        'title', 'category_badge', 'status_badge', 'featured_badge', 
        'views_display', 'youtube_preview', 'published_at'
    ]
    list_filter = ['status', 'category', 'is_featured', 'created_at', 'published_at']
    search_fields = ['title', 'headline', 'description', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['youtube_video_id', 'view_count', 'created_at', 'updated_at']
    list_per_page = 20
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('📝 Basic Information', {
            'fields': ('title', 'slug', 'headline', 'status', 'is_featured'),
            'classes': ['tab']
        }),
        ('🎥 YouTube Video', {
            'fields': ('youtube_url', 'youtube_video_id'),
            'description': 'YouTube video ID will be automatically extracted from the URL.',
            'classes': ['tab']
        }),
        ('📄 Content', {
            'fields': ('description', 'key_points'),
            'classes': ['tab']
        }),
        ('🏷️ Categorization', {
            'fields': ('category', 'tags'),
            'classes': ['tab']
        }),
        ('🔍 SEO & Meta', {
            'fields': ('meta_description',),
            'classes': ['tab']
        }),
        ('📊 Analytics & Timestamps', {
            'fields': ('view_count', 'published_at', 'created_at', 'updated_at'),
            'classes': ['collapse']
        }),
    )
    
    actions = ['make_published', 'make_draft', 'make_featured', 'remove_featured']
    
    @display(description='Preview')
    def youtube_preview(self, obj):
        """Show YouTube thumbnail in admin"""
        if obj.youtube_video_id:
            thumbnail_url = obj.get_youtube_thumbnail_url('default')
            return format_html(
                '<img src="{}" width="80" height="60" style="border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                thumbnail_url
            )
        return format_html('<span style="color: #6b7280;">No video</span>')
    
    @display(description='Category', ordering='category')
    def category_badge(self, obj):
        colors = {
            'exercise': '#3b82f6',       # blue
            'nutrition': '#10b981',      # green
            'wellness': '#8b5cf6',       # purple
            'physiotherapy': '#f59e0b',  # orange
            'general': '#6b7280',        # gray
        }
        color = colors.get(obj.category, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">{}</span>',
            color, obj.get_category_display()
        )
    
    @display(description='Status', ordering='status')
    def status_badge(self, obj):
        if obj.status == 'published':
            return format_html(
                '<span style="background-color: #10b981; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">✅ Published</span>'
            )
        return format_html(
            '<span style="background-color: #6b7280; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">📝 Draft</span>'
        )
    
    @display(description='Featured', ordering='is_featured')
    def featured_badge(self, obj):
        if obj.is_featured:
            return format_html(
                '<span style="background-color: #f59e0b; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">⭐ Featured</span>'
            )
        return format_html('<span style="color: #6b7280;">➖</span>')
    
    @display(description='Views', ordering='view_count')
    def views_display(self, obj):
        return format_html(
            '<span style="background-color: #3b82f6; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">👁️ {}</span>',
            obj.view_count
        )
    
    @admin.action(description='✅ Publish Posts')
    def make_published(self, request, queryset):
        """Bulk action to publish posts"""
        updated = queryset.update(status='published')
        self.message_user(request, f'✅ {updated} posts were marked as published.')
    
    @admin.action(description='📝 Mark as Draft')
    def make_draft(self, request, queryset):
        """Bulk action to make posts draft"""
        updated = queryset.update(status='draft')
        self.message_user(request, f'✅ {updated} posts were marked as draft.')
    
    @admin.action(description='⭐ Mark as Featured')
    def make_featured(self, request, queryset):
        """Bulk action to make posts featured"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'✅ {updated} posts were marked as featured.')
    
    @admin.action(description='➖ Remove Featured')
    def remove_featured(self, request, queryset):
        """Bulk action to remove featured status"""
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'✅ {updated} posts were unmarked as featured.')
