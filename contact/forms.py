from django import forms
from .models import ContactMessage

class ContactMessageForm(forms.ModelForm):
    """
    Contact form for visitors to send messages
    """
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'Enter your full name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'Enter your email address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'Enter your phone number',
                'pattern': '[0-9]{10}',
                'required': True
            }),
            'subject': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'rows': 5,
                'placeholder': 'Enter your message or inquiry',
                'required': True
            }),
        }
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # Remove any non-digit characters
        phone = ''.join(filter(str.isdigit, phone))
        
        if len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        
        return phone