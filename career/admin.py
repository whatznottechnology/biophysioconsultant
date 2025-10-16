from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import JobOpening, JobApplication

@admin.register(JobOpening)
class JobOpeningAdmin(ModelAdmin):
    list_display = ['title', 'training_type_badge', 'location', 'fees_display', 'active_status', 'application_deadline', 'applicant_count']
    list_filter = ['job_type', 'is_active', 'created_at']
    search_fields = ['title', 'location', 'description']
    readonly_fields = ['created_at', 'updated_at', 'applicant_count']
    list_per_page = 20
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('🎓 Basic Information', {
            'fields': ('title', 'description', 'job_type', 'location'),
            'classes': ['tab']
        }),
        ('📋 Requirements & Tuition Fees', {
            'fields': ('requirements', 'salary_min', 'salary_max'),
            'classes': ['tab']
        }),
        ('📅 Application Details', {
            'fields': ('is_active', 'application_deadline', 'applicant_count'),
            'classes': ['tab']
        }),
        ('🕐 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ['collapse']
        }),
    )
    
    @display(description='Clinical Training', ordering='job_type')
    def training_type_badge(self, obj):
        colors = {
            'volunteer': '#8b5cf6',  # purple
            'full_time': '#3b82f6',  # blue
            'part_time': '#10b981',  # green
            'contract': '#f59e0b',   # orange
            'internship': '#ec4899',  # pink
        }
        color = colors.get(obj.job_type, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">{}</span>',
            color, obj.get_job_type_display()
        )
    
    @display(description='Tuition Fees')
    def fees_display(self, obj):
        if obj.salary_min and obj.salary_max:
            return format_html(
                '<span style="color: #10b981; font-weight: 600;">₹{} - ₹{}</span>',
                obj.salary_min, obj.salary_max
            )
        return '-'
    
    @display(description='Status', ordering='is_active')
    def active_status(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color: #10b981; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">✅ Active</span>'
            )
        return format_html(
            '<span style="background-color: #ef4444; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">❌ Inactive</span>'
        )
    
    @display(description='Applications')
    def applicant_count(self, obj):
        count = obj.applications.count()
        return format_html(
            '<span style="background-color: #3b82f6; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">📝 {} Applications</span>',
            count
        )

@admin.register(JobApplication)
class JobApplicationAdmin(ModelAdmin):
    list_display = ['name', 'training_program', 'email', 'whatsapp_number', 'status_badge', 'age_display', 'submitted_at']
    list_filter = ['status', 'sex', 'job_opening', 'submitted_at']
    search_fields = ['name', 'email', 'whatsapp_number', 'job_opening__title', 'qualification']
    readonly_fields = ['submitted_at', 'updated_at', 'age_display']
    list_per_page = 25
    date_hierarchy = 'submitted_at'
    
    fieldsets = (
        ('🎓 Training Application', {
            'fields': ('job_opening', 'status'),
            'classes': ['tab']
        }),
        ('👤 Personal Information', {
            'fields': ('name', 'date_of_birth', 'age_display', 'sex', 'whatsapp_number', 'email'),
            'classes': ['tab']
        }),
        ('🎓 Education & Address', {
            'fields': ('qualification', 'address'),
            'classes': ['tab']
        }),
        ('📝 Admin Notes', {
            'fields': ('admin_notes', 'reviewed_at'),
            'classes': ['tab']
        }),
        ('🕐 Timestamps', {
            'fields': ('submitted_at', 'updated_at'),
            'classes': ['collapse']
        }),
    )
    
    actions = ['mark_as_under_review', 'mark_as_shortlisted', 'mark_as_selected', 'mark_as_rejected']
    
    @display(description='Training Program')
    def training_program(self, obj):
        return format_html(
            '<strong style="color: #3b82f6;">{}</strong><br><small style="color: #6b7280;">{}</small>',
            obj.job_opening.title,
            obj.job_opening.get_job_type_display()
        )
    
    @display(description='Status', ordering='status')
    def status_badge(self, obj):
        colors = {
            'submitted': '#3b82f6',      # blue
            'under_review': '#f59e0b',   # orange
            'shortlisted': '#8b5cf6',    # purple
            'interview_scheduled': '#06b6d4',  # cyan
            'selected': '#10b981',       # green
            'rejected': '#ef4444',       # red
            'withdrawn': '#6b7280',      # gray
        }
        icons = {
            'submitted': '📝',
            'under_review': '👀',
            'shortlisted': '⭐',
            'interview_scheduled': '📅',
            'selected': '✅',
            'rejected': '❌',
            'withdrawn': '🚫',
        }
        color = colors.get(obj.status, '#6b7280')
        icon = icons.get(obj.status, '📄')
        label = obj.get_status_display()
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">{} {}</span>',
            color, icon, label
        )
    
    @display(description='Age')
    def age_display(self, obj):
        from datetime import date
        today = date.today()
        age = today.year - obj.date_of_birth.year - ((today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))
        return format_html(
            '<span style="background-color: #f3f4f6; padding: 4px 12px; border-radius: 8px; font-weight: 600;">{} years</span>',
            age
        )
    
    @admin.action(description='👀 Mark as Under Review')
    def mark_as_under_review(self, request, queryset):
        updated = queryset.update(status='under_review')
        self.message_user(request, f'✅ {updated} applications marked as under review.')
    
    @admin.action(description='⭐ Mark as Shortlisted')
    def mark_as_shortlisted(self, request, queryset):
        updated = queryset.update(status='shortlisted')
        self.message_user(request, f'✅ {updated} applications marked as shortlisted.')
    
    @admin.action(description='✅ Mark as Selected')
    def mark_as_selected(self, request, queryset):
        updated = queryset.update(status='selected')
        self.message_user(request, f'✅ {updated} applications marked as selected.')
    
    @admin.action(description='❌ Mark as Rejected')
    def mark_as_rejected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'✅ {updated} applications marked as rejected.')
