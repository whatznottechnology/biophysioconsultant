from django import forms
from .models import Booking, PrescriptionUpload, Service
from django.utils import timezone
from datetime import datetime, timedelta

class BookingForm(forms.ModelForm):
    """
    Form for creating new bookings (simplified - no date/time selection)
    """
    
    class Meta:
        model = Booking
        fields = [
            'service', 'patient_name', 'patient_age', 
            'patient_phone', 'patient_email', 'symptoms'
        ]
        
        widgets = {
            'service': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'required': True
            }),
            'patient_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'Enter full name',
                'required': True
            }),
            'patient_age': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'min': '1',
                'max': '120',
                'required': True
            }),
            'patient_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'Enter phone number',
                'pattern': '[0-9]{10}',
                'required': True
            }),
            'patient_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'Enter email address (optional)'
            }),
            'symptoms': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'rows': 4,
                'placeholder': 'Describe your symptoms or reason for visit (optional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set service choices
        self.fields['service'].queryset = Service.objects.filter(is_active=True)
        self.fields['service'].empty_label = "Select a service"
    
    def clean_patient_phone(self):
        phone = self.cleaned_data['patient_phone']
        # Remove any non-digit characters
        phone = ''.join(filter(str.isdigit, phone))
        
        if len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        
        return phone
    
    def clean_patient_age(self):
        age = self.cleaned_data['patient_age']
        
        if age < 1 or age > 120:
            raise forms.ValidationError("Age must be between 1 and 120.")
        
        return age

class PrescriptionUploadForm(forms.ModelForm):
    """
    Form for uploading prescriptions and medical reports
    """
    
    class Meta:
        model = PrescriptionUpload
        fields = ['file', 'description']
        
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'accept': '.pdf,.jpg,.jpeg,.png',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'rows': 3,
                'placeholder': 'Describe the uploaded file (e.g., Blood test report, X-ray, Previous prescription)',
                'required': True
            }),
        }
    
    def clean_file(self):
        file = self.cleaned_data['file']
        
        # Check file size (max 10MB)
        if file.size > 10 * 1024 * 1024:
            raise forms.ValidationError("File size cannot exceed 10MB.")
        
        # Check file type
        allowed_types = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png']
        if file.content_type not in allowed_types:
            raise forms.ValidationError("Only PDF, JPG, JPEG, and PNG files are allowed.")
        
        return file

class BookingStepForm(forms.Form):
    """
    Multi-step booking form for better UX
    """
    
    # Step 1: Service Selection
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True),
        empty_label="Select a service",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary'
        })
    )
    
    # Step 2: Date and Time
    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary'
        })
    )
    
    appointment_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary'
        })
    )
    
    # Step 3: Patient Information
    patient_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
            'placeholder': 'Enter full name'
        })
    )
    
    patient_age = forms.IntegerField(
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary'
        })
    )
    
    patient_gender = forms.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary'
        })
    )
    
    patient_phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
            'placeholder': 'Enter phone number'
        })
    )
    
    patient_whatsapp = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
            'placeholder': 'Enter WhatsApp number (optional)'
        })
    )
    
    # Step 4: Health Information
    present_complaints = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
            'rows': 4,
            'placeholder': 'Describe your current health issues and symptoms'
        })
    )
    
    medical_history = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
            'rows': 3,
            'placeholder': 'Previous medical history, medications, allergies (optional)'
        })
    )