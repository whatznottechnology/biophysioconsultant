from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import SiteSettings, Testimonial, PaymentSettings, CustomPage

@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    fieldsets = (
        ('🏥 Site Information', {
            'fields': (
                'site_name', 'site_tagline', 'site_description', 
                'site_logo', 'site_favicon'
            ),
            'classes': ['tab']
        }),
        ('🔍 SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ['tab']
        }),
        ('📞 Contact Information', {
            'fields': ('contact_phone', 'contact_email', 'contact_address'),
            'classes': ['tab']
        }),
        ('📱 Social Media', {
            'fields': (
                'facebook_url', 'twitter_url', 'instagram_url', 
                'linkedin_url', 'youtube_url'
            ),
            'classes': ['tab']
        }),
        ('⚙️ Business Settings', {
            'fields': (
                'practice_start_year', 'consultation_fee', 'is_booking_enabled', 'is_payment_enabled',
                'booking_advance_days', 'booking_cancel_hours'
            ),
            'classes': ['tab']
        }),
        ('📧 Email Settings', {
            'fields': (
                'admin_email', 'send_booking_notifications', 
                'send_reminder_notifications'
            ),
            'classes': ['tab']
        }),
        ('🔧 Maintenance', {
            'fields': ('maintenance_mode', 'maintenance_message'),
            'classes': ['tab']
        }),
        ('📊 Analytics & Tracking', {
            'fields': (
                'google_analytics_id', 'google_tag_manager_id', 'facebook_pixel_id'
            ),
            'classes': ['tab']
        }),
        ('📱 PWA Settings', {
            'fields': (
                'pwa_app_name', 'pwa_short_name', 'pwa_theme_color', 
                'pwa_background_color'
            ),
            'classes': ['tab']
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False

@admin.register(Testimonial)
class TestimonialAdmin(ModelAdmin):
    list_display = (
        'patient_name', 'patient_location', 'treatment_for', 
        'rating_stars', 'featured_badge', 'approval_badge', 'created_at'
    )
    list_filter = ('rating', 'is_featured', 'is_approved', 'created_at')
    search_fields = ('patient_name', 'patient_location', 'treatment_for', 'testimonial')
    ordering = ('-created_at',)
    list_per_page = 20
    
    fieldsets = (
        ('👤 Patient Information', {
            'fields': ('patient_name', 'patient_location', 'patient_image'),
            'classes': ['tab']
        }),
        ('💬 Testimonial Details', {
            'fields': ('treatment_for', 'testimonial', 'rating'),
            'classes': ['tab']
        }),
        ('⚙️ Display Settings', {
            'fields': ('is_featured', 'is_approved'),
            'classes': ['tab']
        }),
    )
    
    actions = ['approve_testimonials', 'feature_testimonials', 'unfeature_testimonials']
    
    @display(description='Rating', ordering='rating')
    def rating_stars(self, obj):
        stars = '⭐' * obj.rating
        return format_html(
            '<span style="background-color: #f59e0b; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">{}</span>',
            stars
        )
    
    @display(description='Featured', ordering='is_featured')
    def featured_badge(self, obj):
        if obj.is_featured:
            return format_html(
                '<span style="background-color: #f59e0b; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">⭐ Featured</span>'
            )
        return format_html('<span style="color: #6b7280;">➖</span>')
    
    @display(description='Approval', ordering='is_approved')
    def approval_badge(self, obj):
        if obj.is_approved:
            return format_html(
                '<span style="background-color: #10b981; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">✅ Approved</span>'
            )
        return format_html(
            '<span style="background-color: #ef4444; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">⏳ Pending</span>'
        )
    
    @admin.action(description='✅ Approve Testimonials')
    def approve_testimonials(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'✅ {updated} testimonials approved.')
    
    @admin.action(description='⭐ Feature on Homepage')
    def feature_testimonials(self, request, queryset):
        updated = queryset.update(is_featured=True, is_approved=True)
        self.message_user(request, f'✅ {updated} testimonials featured on homepage.')
    
    @admin.action(description='➖ Remove from Homepage')
    def unfeature_testimonials(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'✅ {updated} testimonials removed from homepage.')


@admin.register(PaymentSettings)
class PaymentSettingsAdmin(ModelAdmin):
    fieldsets = (
        ('💳 Payment Gateway', {
            'fields': ('gateway', 'is_enabled', 'is_test_mode'),
            'classes': ['tab']
        }),
        ('🔐 Razorpay Configuration', {
            'fields': ('razorpay_key_id', 'razorpay_key_secret'),
            'description': 'Enter your Razorpay API credentials',
            'classes': ['tab']
        }),
        ('⚙️ Payment Configuration', {
            'fields': (
                'currency', 'minimum_amount', 
                'convenience_fee_percent', 'convenience_fee_fixed'
            ),
            'classes': ['tab']
        }),
        ('💰 Payment Methods', {
            'fields': (
                'enable_netbanking', 'enable_cards', 'enable_wallets', 
                'enable_upi', 'enable_emi'
            ),
            'classes': ['tab']
        }),
        ('🔗 URLs & Webhooks', {
            'fields': (
                'webhook_url', 'success_url', 'failure_url'
            ),
            'classes': ['tab']
        }),
        ('🏢 Business Information', {
            'fields': (
                'business_name', 'business_logo', 'terms_url', 'privacy_url'
            ),
            'classes': ['tab']
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not PaymentSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False


@admin.register(CustomPage)
class CustomPageAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'active_badge', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug', 'content')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    list_per_page = 20
    
    fieldsets = (
        ('📄 Page Information', {
            'fields': ('name', 'slug', 'content'),
            'classes': ['tab']
        }),
        ('🔍 SEO Settings', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ['tab']
        }),
        ('⚙️ Display Settings', {
            'fields': ('is_active', 'order'),
            'classes': ['tab']
        }),
    )
    
    @display(description='Active', ordering='is_active')
    def active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color: #10b981; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">✅ Active</span>'
            )
        return format_html(
            '<span style="background-color: #6b7280; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">❌ Inactive</span>'
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
