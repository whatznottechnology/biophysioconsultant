from django.db import models
from django.core.validators import RegexValidator, ValidationError
from django.utils import timezone

class SiteSettings(models.Model):
    """
    Global site settings and configuration
    """
    # Site basic information
    site_name = models.CharField(
        max_length=200, 
        default="Bio-Physio Consultant"
    )
    
    site_tagline = models.CharField(
        max_length=500, 
        default="Holistic Health & Physiotherapy Services"
    )
    
    site_description = models.TextField(
        default="Professional healthcare services including physiotherapy, acupressure, massage therapy, and alternative medicine by certified practitioner Pratap Bag."
    )
    
    site_logo = models.ImageField(
        upload_to='site/', 
        blank=True, 
        null=True,
        help_text="Site logo (recommended: 200x200px)"
    )
    
    site_favicon = models.ImageField(
        upload_to='site/', 
        blank=True, 
        null=True,
        help_text="Site favicon (recommended: 32x32px)"
    )
    
    # SEO settings
    meta_title = models.CharField(
        max_length=200, 
        blank=True,
        help_text="Meta title for SEO"
    )
    
    meta_description = models.TextField(
        blank=True,
        help_text="Meta description for SEO"
    )
    
    meta_keywords = models.TextField(
        blank=True,
        help_text="Meta keywords for SEO (comma separated)"
    )
    
    # Contact information
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    contact_phone = models.CharField(
        validators=[phone_regex], 
        max_length=17,
        blank=True
    )
    
    contact_email = models.EmailField(blank=True)
    contact_address = models.TextField(blank=True)
    
    # Social media links
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    
    # Business settings
    practice_start_year = models.PositiveIntegerField(
        default=1998,
        help_text="Year when practice started (used to calculate years of experience)"
    )
    
    consultation_fee = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=200.00,
        help_text="Default consultation fee in INR"
    )
    
    is_booking_enabled = models.BooleanField(
        default=True,
        help_text="Enable/disable online booking"
    )
    
    is_payment_enabled = models.BooleanField(
        default=True,
        help_text="Enable/disable online payment"
    )
    
    booking_advance_days = models.PositiveIntegerField(
        default=30,
        help_text="Maximum days in advance for booking"
    )
    
    booking_cancel_hours = models.PositiveIntegerField(
        default=24,
        help_text="Minimum hours before appointment to cancel"
    )
    
    # Email notifications
    admin_email = models.EmailField(
        blank=True,
        help_text="Admin email for notifications"
    )
    
    send_booking_notifications = models.BooleanField(
        default=True,
        help_text="Send email notifications for new bookings"
    )
    
    send_reminder_notifications = models.BooleanField(
        default=True,
        help_text="Send appointment reminder emails"
    )
    
    # Maintenance mode
    maintenance_mode = models.BooleanField(
        default=False,
        help_text="Enable maintenance mode"
    )
    
    maintenance_message = models.TextField(
        blank=True,
        default="Site is under maintenance. Please check back later.",
        help_text="Message to show during maintenance"
    )
    
    # Google Analytics and tracking
    google_analytics_id = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Google Analytics tracking ID"
    )
    
    google_tag_manager_id = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Google Tag Manager ID"
    )
    
    facebook_pixel_id = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Facebook Pixel ID"
    )
    
    # PWA settings
    pwa_app_name = models.CharField(
        max_length=200, 
        default="Pratap Bag Healthcare"
    )
    
    pwa_short_name = models.CharField(
        max_length=50, 
        default="PB Healthcare"
    )
    
    pwa_theme_color = models.CharField(
        max_length=7, 
        default="#10B981",
        help_text="PWA theme color (hex code)"
    )
    
    pwa_background_color = models.CharField(
        max_length=7, 
        default="#ffffff",
        help_text="PWA background color (hex code)"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError('Only one SiteSettings instance allowed')
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get or create site settings"""
        settings, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'Bio-Physio Consultant',
                'site_tagline': 'Holistic Health & Physiotherapy Services',
            }
        )
        return settings


class CustomPage(models.Model):
    """
    Custom pages that can be created and displayed in footer
    """
    name = models.CharField(
        max_length=100,
        help_text="Page name (will be displayed in footer menu)"
    )
    
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text="URL slug for the page"
    )
    
    content = models.TextField(
        help_text="Page content (supports HTML)"
    )
    
    meta_title = models.CharField(
        max_length=200,
        blank=True,
        help_text="SEO meta title"
    )
    
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="SEO meta description"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Show in footer menu"
    )
    
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order in footer menu"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Custom Page"
        verbose_name_plural = "Custom Pages"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('page_detail', kwargs={'slug': self.slug})


class Testimonial(models.Model):
    """
    Patient testimonials and reviews
    """
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    patient_name = models.CharField(max_length=100)
    patient_location = models.CharField(
        max_length=100, 
        blank=True,
        help_text="City or location"
    )
    
    treatment_for = models.CharField(
        max_length=200,
        help_text="What condition was treated"
    )
    
    testimonial = models.TextField()
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=5)
    
    patient_image = models.ImageField(
        upload_to='testimonials/', 
        blank=True, 
        null=True,
        help_text="Patient photo (optional)"
    )
    
    is_featured = models.BooleanField(
        default=False,
        help_text="Show on homepage"
    )
    
    is_approved = models.BooleanField(
        default=False,
        help_text="Approved for display"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.patient_name} - {self.rating} stars"


class PaymentSettings(models.Model):
    """
    Payment gateway configuration
    """
    PAYMENT_GATEWAY_CHOICES = [
        ('razorpay', 'Razorpay'),
        ('payu', 'PayU'),
        ('paytm', 'Paytm'),
        ('stripe', 'Stripe'),
    ]
    
    gateway = models.CharField(
        max_length=20,
        choices=PAYMENT_GATEWAY_CHOICES,
        default='razorpay'
    )
    
    is_enabled = models.BooleanField(
        default=True,
        help_text="Enable/disable online payments"
    )
    
    is_test_mode = models.BooleanField(
        default=True,
        help_text="Use test/sandbox mode"
    )
    
    # Razorpay settings
    razorpay_key_id = models.CharField(
        max_length=200,
        blank=True,
        help_text="Razorpay Key ID"
    )
    
    razorpay_key_secret = models.CharField(
        max_length=200,
        blank=True,
        help_text="Razorpay Key Secret"
    )
    
    # Payment configuration
    currency = models.CharField(
        max_length=3,
        default='INR',
        help_text="Payment currency code"
    )
    
    minimum_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=100.00,
        help_text="Minimum payment amount"
    )
    
    # Payment fees
    convenience_fee_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text="Convenience fee percentage"
    )
    
    convenience_fee_fixed = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Fixed convenience fee amount"
    )
    
    # Payment options
    enable_netbanking = models.BooleanField(default=True)
    enable_cards = models.BooleanField(default=True)
    enable_wallets = models.BooleanField(default=True)
    enable_upi = models.BooleanField(default=True)
    enable_emi = models.BooleanField(default=False)
    
    # Webhooks and notifications
    webhook_url = models.URLField(
        blank=True,
        help_text="Webhook URL for payment updates"
    )
    
    success_url = models.URLField(
        blank=True,
        help_text="Success redirect URL"
    )
    
    failure_url = models.URLField(
        blank=True,
        help_text="Failure redirect URL"
    )
    
    # Business details for payments
    business_name = models.CharField(
        max_length=200,
        default="Pratap Bag Healthcare",
        help_text="Business name on payment page"
    )
    
    business_logo = models.ImageField(
        upload_to='payment/',
        blank=True,
        null=True,
        help_text="Logo to show on payment page"
    )
    
    terms_url = models.URLField(
        blank=True,
        help_text="Terms and conditions URL"
    )
    
    privacy_url = models.URLField(
        blank=True,
        help_text="Privacy policy URL"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Payment Settings"
        verbose_name_plural = "Payment Settings"
    
    def __str__(self):
        return f"{self.gateway.title()} Payment Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and PaymentSettings.objects.exists():
            raise ValidationError('Only one PaymentSettings instance allowed')
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get or create payment settings"""
        settings, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'gateway': 'razorpay',
                'is_enabled': True,
                'is_test_mode': True,
                'currency': 'INR',
                'business_name': 'Pratap Bag Healthcare',
            }
        )
        return settings
