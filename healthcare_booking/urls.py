"""
Healthcare Booking System URLs
URL configuration for the healthcare booking project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Admin site customization
admin.site.site_header = "Bio-Physio Consultant Admin"
admin.site.site_title = "Bio-Physio Admin"
admin.site.index_title = "Welcome to Bio-Physio Administration"

urlpatterns = [
    # Admin URLs
    path('admin/', admin.site.urls),
    
    # App URLs
    path('', include('bookings.urls')),  # Home page and booking
    path('accounts/', include('accounts.urls')),  # User authentication
    path('blog/', include('blog.urls')),  # Health blog
    path('contact/', include('contact.urls')),  # Contact and clinic info
    path('career/', include('career.urls')),  # Career and training
    path('', include('site_settings.urls')),  # Custom pages
    
    # PWA URLs
    path('manifest.json', TemplateView.as_view(
        template_name='pwa/manifest.json', 
        content_type='application/json'
    ), name='manifest'),
    
    path('sw.js', TemplateView.as_view(
        template_name='pwa/sw.js', 
        content_type='application/javascript'
    ), name='sw'),
    
    # API URLs (for future use)
    path('api/', include('bookings.api_urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
