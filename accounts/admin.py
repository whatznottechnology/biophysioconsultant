from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    
    list_display = (
        'username', 'email', 'full_name_display', 
        'phone_number', 'patient_badge', 'staff_badge', 'date_joined'
    )
    
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 'is_patient',
        'gender', 'date_joined'
    )
    
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    
    ordering = ('-date_joined',)
    list_per_page = 25
    date_hierarchy = 'date_joined'
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('👤 Personal Information', {
            'fields': (
                'phone_number', 'whatsapp_number', 'age', 'gender', 
                'date_of_birth', 'address', 'city', 'state', 'pincode'
            ),
            'classes': ['tab']
        }),
        ('🚨 Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone'),
            'classes': ['tab']
        }),
        ('👨‍⚕️ User Type', {
            'fields': ('is_patient',),
            'classes': ['tab']
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('👤 Personal Information', {
            'fields': (
                'first_name', 'last_name', 'email', 'phone_number', 
                'whatsapp_number', 'is_patient'
            ),
            'classes': ['tab']
        }),
    )
    
    @display(description='Full Name')
    def full_name_display(self, obj):
        if obj.first_name or obj.last_name:
            return format_html(
                '<strong>{} {}</strong>',
                obj.first_name, obj.last_name
            )
        return '-'
    
    @display(description='Patient', ordering='is_patient')
    def patient_badge(self, obj):
        if obj.is_patient:
            return format_html(
                '<span style="background-color: #3b82f6; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">👤 Patient</span>'
            )
        return format_html(
            '<span style="background-color: #6b7280; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">➖ User</span>'
        )
    
    @display(description='Staff', ordering='is_staff')
    def staff_badge(self, obj):
        if obj.is_superuser:
            return format_html(
                '<span style="background-color: #ef4444; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">👑 Superuser</span>'
            )
        elif obj.is_staff:
            return format_html(
                '<span style="background-color: #10b981; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">👨‍💼 Staff</span>'
            )
        return format_html(
            '<span style="background-color: #6b7280; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">➖ Regular</span>'
        )
