from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(forms.ModelForm):
    """
    Simplified user registration form - just email and password
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500',
            'placeholder': 'Enter your email address'
        }),
        help_text="We'll use this email to contact you about your appointments."
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500',
            'placeholder': 'Create a password'
        }),
        help_text="Your password must be at least 8 characters long."
    )
    
    class Meta:
        model = User
        fields = ('email', 'password')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email
    
    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.username = self.cleaned_data["email"]  # Use email as username
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    """
    User profile edit form
    """
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 'whatsapp_number',
            'age', 'gender', 'date_of_birth', 'address', 'city', 'state', 'pincode',
            'emergency_contact_name', 'emergency_contact_phone'
        ]
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'Enter your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'Enter your last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'Enter your email address'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'Enter your phone number',
                'pattern': '[0-9]{10}'
            }),
            'whatsapp_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'Enter your WhatsApp number',
                'pattern': '[0-9]{10}'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'min': '1',
                'max': '120'
            }),
            'gender': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'rows': 3,
                'placeholder': 'Enter your complete address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'Enter your city'
            }),
            'state': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'Enter your state'
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'Enter your pincode',
                'pattern': '[0-9]{6}'
            }),
            'emergency_contact_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'Emergency contact name'
            }),
            'emergency_contact_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'Emergency contact phone',
                'pattern': '[0-9]{10}'
            }),
        }
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone or phone == '':
            return None
            
        # Remove any non-digit characters
        phone = ''.join(filter(str.isdigit, str(phone)))
        
        if not phone:  # After cleaning, if empty
            return None
        
        if len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        
        # Check if another user has this phone (excluding current user)
        if User.objects.filter(phone_number=phone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A user with this phone number already exists.")
        
        return phone
    
    def clean_whatsapp_number(self):
        whatsapp = self.cleaned_data.get('whatsapp_number')
        if not whatsapp or whatsapp == '':
            return None
            
        # Remove any non-digit characters
        whatsapp = ''.join(filter(str.isdigit, str(whatsapp)))
        
        if not whatsapp:  # After cleaning, if empty
            return None
        
        if len(whatsapp) != 10:
            raise forms.ValidationError("WhatsApp number must be exactly 10 digits.")
        
        return whatsapp
    
    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if not pincode or pincode == '':
            return None
            
        # Remove any non-digit characters
        pincode = ''.join(filter(str.isdigit, str(pincode)))
        
        if not pincode:  # After cleaning, if empty
            return None
        
        if len(pincode) != 6:
            raise forms.ValidationError("Pincode must be exactly 6 digits.")
        
        return pincode
    
    def clean_emergency_contact_phone(self):
        phone = self.cleaned_data.get('emergency_contact_phone')
        if not phone or phone == '':
            return None
            
        # Remove any non-digit characters
        phone = ''.join(filter(str.isdigit, str(phone)))
        
        if not phone:  # After cleaning, if empty
            return None
        
        if len(phone) != 10:
            raise forms.ValidationError("Emergency contact phone must be exactly 10 digits.")
        
        return phone