from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    
    list_display = (
        'username', 'email', 'first_name', 'last_name', 
        'phone_number', 'is_patient', 'is_staff', 'date_joined'
    )
    
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 'is_patient',
        'gender', 'date_joined'
    )
    
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Personal Information', {
            'fields': (
                'phone_number', 'whatsapp_number', 'age', 'gender', 
                'date_of_birth', 'address', 'city', 'state', 'pincode'
            )
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
        ('User Type', {
            'fields': ('is_patient',)
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Personal Information', {
            'fields': (
                'first_name', 'last_name', 'email', 'phone_number', 
                'whatsapp_number', 'is_patient'
            )
        }),
    )
