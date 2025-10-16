from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import Service, Booking, PrescriptionUpload

@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = (
        'name', 'price_display', 'duration_minutes', 'prescription_badge', 
        'active_status', 'created_at'
    )
    list_filter = ('is_active', 'requires_prescription', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    list_per_page = 20
    
    fieldsets = (
        ('💊 Service Information', {
            'fields': ('name', 'description', 'duration_minutes'),
            'classes': ['tab']
        }),
        ('💰 Pricing & Requirements', {
            'fields': ('price', 'requires_prescription'),
            'classes': ['tab']
        }),
        ('✅ Status', {
            'fields': ('is_active',),
            'classes': ['tab']
        }),
    )
    
    @display(description='Price')
    def price_display(self, obj):
        return format_html(
            '<span style="color: #10b981; font-weight: 600; font-size: 14px;">₹{}</span>',
            obj.price
        )
    
    @display(description='Prescription', ordering='requires_prescription')
    def prescription_badge(self, obj):
        if obj.requires_prescription:
            return format_html(
                '<span style="background-color: #f59e0b; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">📋 Required</span>'
            )
        return format_html(
            '<span style="background-color: #6b7280; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">➖ Not Required</span>'
        )
    
    @display(description='Status', ordering='is_active')
    def active_status(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color: #10b981; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">✅ Active</span>'
            )
        return format_html(
            '<span style="background-color: #ef4444; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">❌ Inactive</span>'
        )

@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    list_display = (
        'booking_id_short', 'patient_name', 'service', 'appointment_date', 
        'appointment_time', 'status_badge', 'payment_badge', 'created_at'
    )
    
    list_filter = (
        'status', 'payment_status', 'service', 'appointment_date', 
        'created_at', 'patient_gender'
    )
    
    search_fields = (
        'patient_name', 'patient_phone', 'patient_whatsapp', 
        'booking_id', 'patient__username', 'patient__email'
    )
    
    ordering = ('-appointment_date', '-appointment_time')
    list_per_page = 25
    date_hierarchy = 'appointment_date'
    
    readonly_fields = ('booking_id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('📅 Booking Information', {
            'fields': (
                'booking_id', 'patient', 'service', 'appointment_date', 
                'appointment_time', 'duration_minutes'
            ),
            'classes': ['tab']
        }),
        ('👤 Patient Details', {
            'fields': (
                'patient_name', 'patient_age', 'patient_gender', 
                'patient_phone', 'patient_whatsapp'
            ),
            'classes': ['tab']
        }),
        ('🏥 Health Information', {
            'fields': ('present_complaints', 'medical_history'),
            'classes': ['tab']
        }),
        ('💳 Status & Payment', {
            'fields': (
                'status', 'payment_status', 'payment_amount', 'payment_id'
            ),
            'classes': ['tab']
        }),
        ('📝 Admin Notes', {
            'fields': ('admin_notes',),
            'classes': ['tab']
        }),
        ('🕐 Timestamps', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'completed_at'),
            'classes': ['collapse']
        }),
    )
    
    actions = ['mark_as_confirmed', 'mark_as_completed', 'mark_as_cancelled']
    
    @display(description='Booking ID')
    def booking_id_short(self, obj):
        return format_html(
            '<span style="font-family: monospace; background-color: #f3f4f6; padding: 4px 8px; border-radius: 6px; font-size: 11px;">{}</span>',
            str(obj.booking_id)[:12] + '...'
        )
    
    @display(description='Status', ordering='status')
    def status_badge(self, obj):
        colors = {
            'pending': '#f59e0b',    # orange
            'confirmed': '#3b82f6',  # blue
            'completed': '#10b981',  # green
            'cancelled': '#ef4444',  # red
            'no_show': '#6b7280',    # gray
        }
        icons = {
            'pending': '⏳',
            'confirmed': '✅',
            'completed': '🎉',
            'cancelled': '❌',
            'no_show': '🚫',
        }
        color = colors.get(obj.status, '#6b7280')
        icon = icons.get(obj.status, '📄')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">{} {}</span>',
            color, icon, obj.get_status_display()
        )
    
    @display(description='Payment', ordering='payment_status')
    def payment_badge(self, obj):
        colors = {
            'pending': '#f59e0b',    # orange
            'completed': '#10b981',  # green
            'failed': '#ef4444',     # red
            'refunded': '#8b5cf6',   # purple
        }
        icons = {
            'pending': '⏳',
            'completed': '💰',
            'failed': '❌',
            'refunded': '↩️',
        }
        color = colors.get(obj.payment_status, '#6b7280')
        icon = icons.get(obj.payment_status, '💳')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">{} {}</span>',
            color, icon, obj.get_payment_status_display()
        )
    
    @admin.action(description='✅ Mark as Confirmed')
    def mark_as_confirmed(self, request, queryset):
        updated = 0
        for booking in queryset:
            if booking.status == 'pending':
                booking.confirm_booking()
                updated += 1
        self.message_user(request, f'✅ {updated} bookings marked as confirmed.')
    
    @admin.action(description='🎉 Mark as Completed')
    def mark_as_completed(self, request, queryset):
        updated = 0
        for booking in queryset:
            if booking.status in ['pending', 'confirmed']:
                booking.complete_booking()
                updated += 1
        self.message_user(request, f'✅ {updated} bookings marked as completed.')
    
    @admin.action(description='❌ Cancel Bookings')
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.filter(
            status__in=['pending', 'confirmed']
        ).update(status='cancelled')
        self.message_user(request, f'✅ {updated} bookings cancelled.')

@admin.register(PrescriptionUpload)
class PrescriptionUploadAdmin(ModelAdmin):
    list_display = (
        'patient_name', 'booking_appointment', 'file_name', 
        'file_size_mb', 'uploaded_at'
    )
    
    list_filter = ('uploaded_at', 'file_type')
    search_fields = ('booking__patient_name', 'patient__username', 'file_name')
    ordering = ('-uploaded_at',)
    
    readonly_fields = ('file_name', 'file_type', 'file_size', 'uploaded_at')
    
    def patient_name(self, obj):
        return obj.booking.patient_name
    patient_name.short_description = 'Patient'
    
    def booking_appointment(self, obj):
        return f"{obj.booking.appointment_date} at {obj.booking.appointment_time}"
    booking_appointment.short_description = 'Appointment'
    
    def file_size_mb(self, obj):
        if obj.file_size:
            return f"{obj.file_size / (1024*1024):.2f} MB"
        return "Unknown"
    file_size_mb.short_description = 'File Size'
