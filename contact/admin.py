from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import ContactMessage, ClinicInfo

@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):
    list_display = (
        'name', 'email', 'phone', 'subject', 'status_badge', 'created_at'
    )
    list_filter = ('status', 'subject', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    ordering = ('-created_at',)
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    readonly_fields = ('created_at', 'updated_at', 'message_preview')
    
    fieldsets = (
        ('📧 Contact Information', {
            'fields': ('name', 'email', 'phone', 'subject'),
            'classes': ['tab']
        }),
        ('💬 Message Details', {
            'fields': ('message', 'message_preview'),
            'classes': ['tab']
        }),
        ('✅ Status & Reply', {
            'fields': ('status', 'admin_reply', 'replied_at'),
            'classes': ['tab']
        }),
        ('🕐 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ['collapse']
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_replied', 'mark_as_new']
    
    @display(description='Status', ordering='status')
    def status_badge(self, obj):
        colors = {
            'new': '#ef4444',  # red
            'read': '#f59e0b',  # orange
            'replied': '#10b981',  # green
            'closed': '#6b7280',  # gray
        }
        labels = {
            'new': '🆕 New',
            'read': '👁️ Read',
            'replied': '✅ Replied',
            'closed': '🔒 Closed',
        }
        color = colors.get(obj.status, '#6b7280')
        label = labels.get(obj.status, obj.status.title())
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">{}</span>',
            color, label
        )
    
    @display(description='Message Preview')
    def message_preview(self, obj):
        if obj.message:
            preview = obj.message[:200] + '...' if len(obj.message) > 200 else obj.message
            return format_html('<div style="background: #f3f4f6; padding: 12px; border-radius: 8px; border-left: 4px solid #10b981;">{}</div>', preview)
        return '-'
    
    @admin.action(description='✅ Mark as Read')
    def mark_as_read(self, request, queryset):
        updated = queryset.filter(status='new').update(status='read')
        self.message_user(request, f'✅ {updated} messages marked as read.')
    
    @admin.action(description='📧 Mark as Replied')
    def mark_as_replied(self, request, queryset):
        updated = queryset.filter(status__in=['new', 'read']).update(status='replied')
        self.message_user(request, f'✅ {updated} messages marked as replied.')
    
    @admin.action(description='🆕 Mark as New')
    def mark_as_new(self, request, queryset):
        updated = queryset.update(status='new')
        self.message_user(request, f'✅ {updated} messages marked as new.')

@admin.register(ClinicInfo)
class ClinicInfoAdmin(ModelAdmin):
    list_display = ('name', 'city', 'phone_primary', 'email_primary', 'active_status')
    list_filter = ('is_active', 'city', 'state')
    search_fields = ('name', 'city', 'phone_primary', 'email_primary')
    
    fieldsets = (
        ('🏥 Basic Information', {
            'fields': ('name', 'is_active'),
            'classes': ['tab']
        }),
        ('📍 Address', {
            'fields': ('address', 'city', 'state', 'pincode', 'country'),
            'classes': ['tab']
        }),
        ('📞 Contact Details', {
            'fields': (
                'phone_primary', 'phone_secondary', 'email_primary', 
                'email_secondary', 'whatsapp_number', 'emergency_contact'
            ),
            'classes': ['tab']
        }),
        ('🗺️ Location & Maps', {
            'fields': ('latitude', 'longitude', 'google_maps_embed_url'),
            'classes': ['tab']
        }),
        ('🕐 Operating Hours', {
            'fields': (
                'monday_hours', 'tuesday_hours', 'wednesday_hours', 
                'thursday_hours', 'friday_hours', 'saturday_hours', 'sunday_hours'
            ),
            'classes': ['tab']
        }),
    )
    
    @display(description='Active Status', ordering='is_active')
    def active_status(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color: #10b981; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">✅ Active</span>'
            )
        return format_html(
            '<span style="background-color: #ef4444; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">❌ Inactive</span>'
        )
