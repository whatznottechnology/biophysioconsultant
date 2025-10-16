"""
Utility functions for Django Unfold admin customization
"""
from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from datetime import datetime, timedelta


def get_site_logo_or_fallback(request):
    """
    Get site logo from settings or return fallback logo
    """
    try:
        from site_settings.models import SiteSettings
        settings = SiteSettings.get_settings()
        
        if settings.site_logo:
            return request.build_absolute_uri(settings.site_logo.url)
        else:
            return static("images/loogoo.png")
    except:
        return static("images/loogoo.png")


def environment_callback(request):
    """
    Callback to determine the environment badge in the admin
    """
    from django.conf import settings
    
    if settings.DEBUG:
        return ["Development", "warning"]  # Orange badge
    return ["Production", "success"]  # Green badge


def dashboard_callback(request, context):
    """
    Callback to add custom dashboard statistics
    """
    from bookings.models import Booking
    from accounts.models import User
    from career.models import JobOpening, JobApplication
    from contact.models import ContactMessage
    
    # Get today's date
    today = datetime.now().date()
    
    # Get statistics
    context.update({
        "navigation": [
            {
                "title": _("Quick Stats"),
                "items": [
                    {
                        "title": _("Total Bookings"),
                        "icon": "calendar_month",
                        "value": Booking.objects.count(),
                        "description": _("All time bookings"),
                    },
                    {
                        "title": _("Today's Bookings"),
                        "icon": "today",
                        "value": Booking.objects.filter(appointment_date=today).count(),
                        "description": _("Bookings scheduled for today"),
                    },
                    {
                        "title": _("Pending Bookings"),
                        "icon": "pending_actions",
                        "value": Booking.objects.filter(status='pending').count(),
                        "description": _("Awaiting confirmation"),
                    },
                    {
                        "title": _("Total Patients"),
                        "icon": "group",
                        "value": User.objects.filter(is_active=True).count(),
                        "description": _("Registered users"),
                    },
                ],
            },
            {
                "title": _("Training & Career"),
                "items": [
                    {
                        "title": _("Active Batches"),
                        "icon": "school",
                        "value": JobOpening.objects.filter(is_active=True).count(),
                        "description": _("Currently accepting applications"),
                    },
                    {
                        "title": _("New Applications"),
                        "icon": "description",
                        "value": JobApplication.objects.filter(status='submitted').count(),
                        "description": _("Pending review"),
                    },
                ],
            },
            {
                "title": _("Messages & Communication"),
                "items": [
                    {
                        "title": _("Unread Messages"),
                        "icon": "mail",
                        "value": ContactMessage.objects.filter(status='new').count(),
                        "description": _("New contact messages"),
                    },
                ],
            },
        ],
    })
    
    return context
