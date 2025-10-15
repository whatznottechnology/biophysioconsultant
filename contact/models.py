from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

class ContactMessage(models.Model):
    """
    Contact form messages from visitors
    """
    SUBJECT_CHOICES = [
        ('appointment', 'Appointment Inquiry'),
        ('service', 'Service Information'),
        ('career', 'Career Inquiry'),
        ('general', 'General Inquiry'),
        ('complaint', 'Complaint'),
        ('feedback', 'Feedback'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('closed', 'Closed'),
    ]
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(
        validators=[phone_regex], 
        max_length=17,
        help_text="Phone number for contact"
    )
    
    subject = models.CharField(
        max_length=20, 
        choices=SUBJECT_CHOICES, 
        default='general'
    )
    
    message = models.TextField()
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='new'
    )
    
    admin_reply = models.TextField(
        blank=True, 
        null=True,
        help_text="Reply from admin"
    )
    
    replied_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_subject_display()}"
    
    def mark_as_read(self):
        """Mark message as read"""
        if self.status == 'new':
            self.status = 'read'
            self.save()
    
    def mark_as_replied(self):
        """Mark message as replied"""
        self.status = 'replied'
        self.replied_at = timezone.now()
        self.save()

class ClinicInfo(models.Model):
    """
    Clinic contact information and details
    """
    name = models.CharField(
        max_length=200, 
        default="Pratap Bag Healthcare Clinic"
    )
    
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default="India")
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    phone_primary = models.CharField(
        validators=[phone_regex], 
        max_length=17
    )
    
    phone_secondary = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        blank=True, 
        null=True
    )
    
    email_primary = models.EmailField()
    email_secondary = models.EmailField(blank=True, null=True)
    
    whatsapp_number = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        blank=True, 
        null=True
    )
    
    # Map and location details
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True,
        help_text="Latitude for Google Maps"
    )
    
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True,
        help_text="Longitude for Google Maps"
    )
    
    google_maps_embed_url = models.URLField(
        max_length=500,
        blank=True, 
        null=True,
        help_text="Google Maps embed URL"
    )
    
    # Operating hours
    monday_hours = models.CharField(max_length=50, default="9:00 AM - 6:00 PM")
    tuesday_hours = models.CharField(max_length=50, default="9:00 AM - 6:00 PM")
    wednesday_hours = models.CharField(max_length=50, default="9:00 AM - 6:00 PM")
    thursday_hours = models.CharField(max_length=50, default="9:00 AM - 6:00 PM")
    friday_hours = models.CharField(max_length=50, default="9:00 AM - 6:00 PM")
    saturday_hours = models.CharField(max_length=50, default="9:00 AM - 6:00 PM")
    sunday_hours = models.CharField(max_length=50, default="Closed")
    
    emergency_contact = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        blank=True, 
        null=True,
        help_text="Emergency contact number"
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Clinic Information"
        verbose_name_plural = "Clinic Information"
    
    def __str__(self):
        return self.name
    
    @property
    def full_address(self):
        """Return the complete address"""
        return f"{self.address}, {self.city}, {self.state} - {self.pincode}, {self.country}"
