from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import BlogPost


class BlogListView(ListView):
    """
    Blog list view showing all published posts
    """
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = BlogPost.objects.filter(status='published')
        
        # Category filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(headline__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(tags__icontains=search_query)
            )
        
        return queryset.order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add featured posts
        context['featured_posts'] = BlogPost.objects.filter(
            status='published', 
            is_featured=True
        )[:3]
        
        # Add categories with post counts
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
        context['categories'] = categories
        
        # Add current filters
        context['current_category'] = self.request.GET.get('category', '')
        context['current_search'] = self.request.GET.get('search', '')
        
        return context


class BlogDetailView(DetailView):
    """
    Blog post detail view
    """
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return BlogPost.objects.filter(status='published')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Increment view count
        obj.increment_view_count()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add related posts (same category, excluding current post)
        context['related_posts'] = BlogPost.objects.filter(
            status='published',
            category=self.object.category
        ).exclude(id=self.object.id)[:4]
        
        # Add latest posts
        context['latest_posts'] = BlogPost.objects.filter(
            status='published'
        ).exclude(id=self.object.id)[:5]
        
        # Add category choices for the sidebar
        context['category_choices'] = BlogPost.CATEGORY_CHOICES
        
        return context


class BlogCategoryView(ListView):
    """
    Category-specific blog posts
    """
    model = BlogPost
    template_name = 'blog/blog_category.html'
    context_object_name = 'posts'
    paginate_by = 12
    
    def get_queryset(self):
        self.category = self.kwargs['category']
        return BlogPost.objects.filter(
            status='published',
            category=self.category
        ).order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get category name
        category_dict = dict(BlogPost.CATEGORY_CHOICES)
        context['category_name'] = category_dict.get(self.category, self.category.title())
        context['category_slug'] = self.category
        
        # Add featured posts from this category
        context['featured_posts'] = self.get_queryset().filter(is_featured=True)[:3]
        
        # Add category choices for sidebar
        context['category_choices'] = BlogPost.CATEGORY_CHOICES
        
        # Add a sample post for accessing model methods if posts exist
        if self.get_queryset().exists():
            context['post'] = self.get_queryset().first()
        
        return context


def blog_search(request):
    """
    AJAX search for blog posts
    """
    query = request.GET.get('q', '')
    
    if len(query) < 3:
        return JsonResponse({'results': []})
    
    posts = BlogPost.objects.filter(
        status='published'
    ).filter(
        Q(title__icontains=query) |
        Q(headline__icontains=query) |
        Q(description__icontains=query) |
        Q(tags__icontains=query)
    )[:10]
    
    results = []
    for post in posts:
        results.append({
            'title': post.title,
            'headline': post.headline,
            'url': post.get_absolute_url(),
            'thumbnail': post.get_youtube_thumbnail_url('default'),
            'category': post.get_category_display(),
            'published_at': post.published_at.strftime('%B %d, %Y') if post.published_at else ''
        })
    
    return JsonResponse({'results': results})
