from django import forms
from .models import JobApplication


class JobApplicationForm(forms.ModelForm):
    """
    Simplified form for job applications
    """
    
    class Meta:
        model = JobApplication
        fields = [
            'name', 'date_of_birth', 'sex', 'whatsapp_number',
            'email', 'qualification', 'address'
        ]
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500',
                'placeholder': 'Enter your full name',
                'required': True
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500',
                'type': 'date',
                'required': True
            }),
            'sex': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500',
                'required': True
            }),
            'whatsapp_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500',
                'placeholder': 'Enter WhatsApp number',
                'pattern': '[0-9+]{10,15}',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500',
                'placeholder': 'Enter your email address',
                'required': True
            }),
            'qualification': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500',
                'placeholder': 'Enter your educational qualification',
                'required': True
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500',
                'rows': 3,
                'placeholder': 'Enter your complete address',
                'required': True
            }),
        }
    
    def clean_whatsapp_number(self):
        number = self.cleaned_data['whatsapp_number']
        # Remove any non-digit characters except +
        number = ''.join(c for c in number if c.isdigit() or c == '+')
        
        if len(number) < 10:
            raise forms.ValidationError("WhatsApp number must be at least 10 digits.")
        
        return number