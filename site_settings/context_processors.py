from .models import SiteSettings, CustomPage
from datetime import datetime

def site_settings(request):
    """
    Context processor to make site settings available in all templates
    """
    try:
        settings = SiteSettings.get_settings()
        
        # Calculate years of experience
        current_year = datetime.now().year
        years_of_experience = current_year - settings.practice_start_year
        
        # Get active custom pages for footer
        custom_pages = CustomPage.objects.filter(is_active=True).order_by('order', 'name')
        
        return {
            'site_settings': settings,
            'years_of_experience': years_of_experience,
            'current_year': current_year,
            'custom_pages': custom_pages,
        }
    except Exception:
        # Return default values if settings don't exist
        current_year = datetime.now().year
        return {
            'site_settings': None,
            'years_of_experience': current_year - 1998,  # Default fallback
            'current_year': current_year,
            'custom_pages': CustomPage.objects.filter(is_active=True).order_by('order', 'name') if CustomPage.objects.exists() else [],
        }