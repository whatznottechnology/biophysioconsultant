from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    """
    Custom User model for the healthcare booking system
    """
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    phone_number = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        blank=True, 
        null=True,
        help_text="Phone number for contact"
    )
    
    whatsapp_number = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        blank=True, 
        null=True,
        help_text="WhatsApp number for communication"
    )
    
    age = models.PositiveIntegerField(
        blank=True, 
        null=True,
        help_text="Age of the user"
    )
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    gender = models.CharField(
        max_length=1, 
        choices=GENDER_CHOICES, 
        blank=True, 
        null=True
    )
    
    date_of_birth = models.DateField(
        blank=True, 
        null=True,
        help_text="Date of birth"
    )
    
    address = models.TextField(
        blank=True, 
        null=True,
        help_text="Complete address"
    )
    
    city = models.CharField(
        max_length=100, 
        blank=True, 
        null=True
    )
    
    state = models.CharField(
        max_length=100, 
        blank=True, 
        null=True
    )
    
    pincode = models.CharField(
        max_length=10, 
        blank=True, 
        null=True
    )
    
    emergency_contact_name = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Emergency contact person name"
    )
    
    emergency_contact_phone = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        blank=True, 
        null=True,
        help_text="Emergency contact phone number"
    )
    
    is_patient = models.BooleanField(
        default=True,
        help_text="Designates whether this user is a patient."
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"
    
    @property
    def full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_display_name(self):
        """Return the display name for the user."""
        if self.full_name:
            return self.full_name
        return self.username
