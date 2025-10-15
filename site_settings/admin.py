from django.contrib import admin
from .models import SiteSettings, Testimonial, PaymentSettings, CustomPage

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Site Information', {
            'fields': (
                'site_name', 'site_tagline', 'site_description', 
                'site_logo', 'site_favicon'
            )
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Contact Information', {
            'fields': ('contact_phone', 'contact_email', 'contact_address')
        }),
        ('Social Media', {
            'fields': (
                'facebook_url', 'twitter_url', 'instagram_url', 
                'linkedin_url', 'youtube_url'
            ),
            'classes': ('collapse',)
        }),
        ('Business Settings', {
            'fields': (
                'practice_start_year', 'consultation_fee', 'is_booking_enabled', 'is_payment_enabled',
                'booking_advance_days', 'booking_cancel_hours'
            )
        }),
        ('Email Settings', {
            'fields': (
                'admin_email', 'send_booking_notifications', 
                'send_reminder_notifications'
            ),
            'classes': ('collapse',)
        }),
        ('Maintenance', {
            'fields': ('maintenance_mode', 'maintenance_message'),
            'classes': ('collapse',)
        }),
        ('Analytics & Tracking', {
            'fields': (
                'google_analytics_id', 'google_tag_manager_id', 'facebook_pixel_id'
            ),
            'classes': ('collapse',)
        }),
        ('PWA Settings', {
            'fields': (
                'pwa_app_name', 'pwa_short_name', 'pwa_theme_color', 
                'pwa_background_color'
            ),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        'patient_name', 'patient_location', 'treatment_for', 
        'rating', 'is_featured', 'is_approved', 'created_at'
    )
    list_filter = ('rating', 'is_featured', 'is_approved', 'created_at')
    search_fields = ('patient_name', 'patient_location', 'treatment_for', 'testimonial')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Patient Information', {
            'fields': ('patient_name', 'patient_location', 'patient_image')
        }),
        ('Testimonial Details', {
            'fields': ('treatment_for', 'testimonial', 'rating')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_approved')
        }),
    )
    
    actions = ['approve_testimonials', 'feature_testimonials', 'unfeature_testimonials']
    
    def approve_testimonials(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} testimonials approved.')
    approve_testimonials.short_description = 'Approve selected testimonials'
    
    def feature_testimonials(self, request, queryset):
        updated = queryset.update(is_featured=True, is_approved=True)
        self.message_user(request, f'{updated} testimonials featured on homepage.')
    feature_testimonials.short_description = 'Feature selected testimonials on homepage'
    
    def unfeature_testimonials(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} testimonials removed from homepage.')
    unfeature_testimonials.short_description = 'Remove from homepage'


@admin.register(PaymentSettings)
class PaymentSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Payment Gateway', {
            'fields': ('gateway', 'is_enabled', 'is_test_mode')
        }),
        ('Razorpay Configuration', {
            'fields': ('razorpay_key_id', 'razorpay_key_secret'),
            'description': 'Enter your Razorpay API credentials'
        }),
        ('Payment Configuration', {
            'fields': (
                'currency', 'minimum_amount', 
                'convenience_fee_percent', 'convenience_fee_fixed'
            )
        }),
        ('Payment Methods', {
            'fields': (
                'enable_netbanking', 'enable_cards', 'enable_wallets', 
                'enable_upi', 'enable_emi'
            ),
            'classes': ('collapse',)
        }),
        ('URLs & Webhooks', {
            'fields': (
                'webhook_url', 'success_url', 'failure_url'
            ),
            'classes': ('collapse',)
        }),
        ('Business Information', {
            'fields': (
                'business_name', 'business_logo', 'terms_url', 'privacy_url'
            ),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not PaymentSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False


@admin.register(CustomPage)
class CustomPageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug', 'content')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    
    fieldsets = (
        ('Page Information', {
            'fields': ('name', 'slug', 'content')
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.meta_title:
            obj.meta_title = obj.name
        if not obj.meta_description and obj.content:
            # Strip HTML and truncate for meta description
            import re
            clean_content = re.sub(r'<[^>]+>', '', obj.content)
            obj.meta_description = (clean_content[:157] + '...') if len(clean_content) > 160 else clean_content
        super().save_model(request, obj, form, change)
