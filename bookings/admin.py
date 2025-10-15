from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Service, Booking, PrescriptionUpload

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'price', 'duration_minutes', 'requires_prescription', 
        'is_active', 'created_at'
    )
    list_filter = ('is_active', 'requires_prescription', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    
    fieldsets = (
        ('Service Information', {
            'fields': ('name', 'description', 'duration_minutes')
        }),
        ('Pricing & Requirements', {
            'fields': ('price', 'requires_prescription')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'booking_id_short', 'patient_name', 'service', 'appointment_date', 
        'appointment_time', 'status', 'payment_status', 'created_at'
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
    
    readonly_fields = ('booking_id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Booking Information', {
            'fields': (
                'booking_id', 'patient', 'service', 'appointment_date', 
                'appointment_time', 'duration_minutes'
            )
        }),
        ('Patient Details', {
            'fields': (
                'patient_name', 'patient_age', 'patient_gender', 
                'patient_phone', 'patient_whatsapp'
            )
        }),
        ('Health Information', {
            'fields': ('present_complaints', 'medical_history')
        }),
        ('Status & Payment', {
            'fields': (
                'status', 'payment_status', 'payment_amount', 'payment_id'
            )
        }),
        ('Admin Notes', {
            'fields': ('admin_notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_confirmed', 'mark_as_completed', 'mark_as_cancelled']
    
    def booking_id_short(self, obj):
        return str(obj.booking_id)[:8] + '...'
    booking_id_short.short_description = 'Booking ID'
    
    def mark_as_confirmed(self, request, queryset):
        updated = 0
        for booking in queryset:
            if booking.status == 'pending':
                booking.confirm_booking()
                updated += 1
        self.message_user(request, f'{updated} bookings marked as confirmed.')
    mark_as_confirmed.short_description = 'Mark selected bookings as confirmed'
    
    def mark_as_completed(self, request, queryset):
        updated = 0
        for booking in queryset:
            if booking.status in ['pending', 'confirmed']:
                booking.complete_booking()
                updated += 1
        self.message_user(request, f'{updated} bookings marked as completed.')
    mark_as_completed.short_description = 'Mark selected bookings as completed'
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.filter(
            status__in=['pending', 'confirmed']
        ).update(status='cancelled')
        self.message_user(request, f'{updated} bookings cancelled.')
    mark_as_cancelled.short_description = 'Cancel selected bookings'

@admin.register(PrescriptionUpload)
class PrescriptionUploadAdmin(admin.ModelAdmin):
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
