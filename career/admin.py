from django.contrib import admin
from .models import JobOpening, JobApplication

@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ['title', 'job_type', 'location', 'salary_range', 'is_active', 'application_deadline']
    list_filter = ['job_type', 'is_active', 'created_at']
    search_fields = ['title', 'location', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'job_type', 'location')
        }),
        ('Requirements & Salary', {
            'fields': ('requirements', 'salary_min', 'salary_max')
        }),
        ('Application Details', {
            'fields': ('is_active', 'application_deadline')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'job_opening', 'email', 'whatsapp_number', 'status', 'date_of_birth', 'submitted_at']
    list_filter = ['status', 'sex', 'job_opening', 'submitted_at']
    search_fields = ['name', 'email', 'whatsapp_number', 'job_opening__title']
    readonly_fields = ['submitted_at', 'updated_at']
    fieldsets = (
        ('Job Application', {
            'fields': ('job_opening', 'status')
        }),
        ('Personal Information', {
            'fields': ('name', 'date_of_birth', 'sex', 'whatsapp_number', 'email')
        }),
        ('Education & Address', {
            'fields': ('qualification', 'address')
        }),
        ('Admin Notes', {
            'fields': ('admin_notes', 'reviewed_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
