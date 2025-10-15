from django.contrib import admin
from .models import ContactMessage, ClinicInfo

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'phone', 'subject', 'status', 'created_at'
    )
    list_filter = ('status', 'subject', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    ordering = ('-created_at',)
    
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'subject')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status & Reply', {
            'fields': ('status', 'admin_reply', 'replied_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_replied']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.filter(status='new').update(status='read')
        self.message_user(request, f'{updated} messages marked as read.')
    mark_as_read.short_description = 'Mark selected messages as read'
    
    def mark_as_replied(self, request, queryset):
        updated = queryset.filter(status__in=['new', 'read']).update(status='replied')
        self.message_user(request, f'{updated} messages marked as replied.')
    mark_as_replied.short_description = 'Mark selected messages as replied'

@admin.register(ClinicInfo)
class ClinicInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'phone_primary', 'email_primary', 'is_active')
    list_filter = ('is_active', 'city', 'state')
    search_fields = ('name', 'city', 'phone_primary', 'email_primary')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'is_active')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'pincode', 'country')
        }),
        ('Contact Details', {
            'fields': (
                'phone_primary', 'phone_secondary', 'email_primary', 
                'email_secondary', 'whatsapp_number', 'emergency_contact'
            )
        }),
        ('Location & Maps', {
            'fields': ('latitude', 'longitude', 'google_maps_embed_url')
        }),
        ('Operating Hours', {
            'fields': (
                'monday_hours', 'tuesday_hours', 'wednesday_hours', 
                'thursday_hours', 'friday_hours', 'saturday_hours', 'sunday_hours'
            )
        }),
    )
