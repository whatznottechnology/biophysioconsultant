from django import template
from django.db.models import Count
from blog.models import BlogPost

register = template.Library()

@register.simple_tag
def get_category_counts():
    """Get all categories with their post counts"""
    categories = []
    for choice in BlogPost.CATEGORY_CHOICES:
        count = BlogPost.objects.filter(
            status='published',
            category=choice[0]
        ).count()
        if count > 0:
            categories.append({
                'slug': choice[0],
                'name': choice[1],
                'count': count
            })
    return categories

@register.simple_tag
def get_featured_posts(category=None, limit=3):
    """Get featured posts, optionally filtered by category"""
    queryset = BlogPost.objects.filter(
        status='published',
        is_featured=True
    )
    
    if category:
        queryset = queryset.filter(category=category)
    
    return queryset[:limit]

@register.simple_tag
def get_latest_posts(exclude_id=None, limit=5):
    """Get latest published posts"""
    queryset = BlogPost.objects.filter(status='published')
    
    if exclude_id:
        queryset = queryset.exclude(id=exclude_id)
    
    return queryset.order_by('-published_at')[:limit]

@register.simple_tag
def get_related_posts(post, limit=4):
    """Get related posts from the same category"""
    return BlogPost.objects.filter(
        status='published',
        category=post.category
    ).exclude(id=post.id)[:limit]

@register.filter
def get_tags_list(post):
    """Get tags as a list"""
    if hasattr(post, 'tags') and post.tags:
        return [tag.strip() for tag in post.tags.split(',') if tag.strip()]
    return []

@register.filter
def get_key_points_list(post):
    """Get key points as a list"""
    if hasattr(post, 'key_points') and post.key_points:
        return [point.strip() for point in post.key_points.split('\n') if point.strip()]
    return []

# Alternative approach - register the same filters as simple tags
@register.simple_tag
def post_tags_list(post):
    """Get tags as a list - simple tag version"""
    if hasattr(post, 'tags') and post.tags:
        return [tag.strip() for tag in post.tags.split(',') if tag.strip()]
    return []

@register.simple_tag
def post_key_points_list(post):
    """Get key points as a list - simple tag version"""
    if hasattr(post, 'key_points') and post.key_points:
        return [point.strip() for point in post.key_points.split('\n') if point.strip()]
    return []

@register.filter
def split(value, delimiter=','):
    """Split a string by delimiter"""
    if value:
        return [item.strip() for item in value.split(delimiter) if item.strip()]
    return []