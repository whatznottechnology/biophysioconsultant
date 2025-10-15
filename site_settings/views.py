from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import CustomPage

class CustomPageView(DetailView):
    """
    View for displaying custom pages
    """
    model = CustomPage
    template_name = 'site_settings/custom_page.html'
    context_object_name = 'page'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return CustomPage.objects.filter(is_active=True)

def page_detail(request, slug):
    """
    Function-based view for custom page detail
    """
    page = get_object_or_404(CustomPage, slug=slug, is_active=True)
    
    context = {
        'page': page,
        'title': page.meta_title or page.name,
        'meta_description': page.meta_description,
    }
    
    return render(request, 'site_settings/custom_page.html', context)