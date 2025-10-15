from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()

class Service(models.Model):
    """
    Healthcare services offered by Pratap Bag
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    duration_minutes = models.PositiveIntegerField(
        default=30,
        help_text="Duration of the service in minutes"
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=200.00,
        help_text="Service price in INR"
    )
    is_active = models.BooleanField(default=True)
    requires_prescription = models.BooleanField(
        default=False,
        help_text="Whether this service requires prescription upload"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Booking(models.Model):
    """
    Patient appointment bookings
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    # Unique booking ID
    booking_id = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        unique=True
    )
    
    # Patient information (optional - for guests)
    patient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='bookings',
        null=True,
        blank=True
    )
    
    # Service details
    service = models.ForeignKey(
        Service, 
        on_delete=models.CASCADE, 
        related_name='bookings'
    )
    
    # Appointment details (optional - to be scheduled later)
    appointment_date = models.DateField(null=True, blank=True)
    appointment_time = models.TimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(default=30)
    
    # Patient details (can be different from user profile)
    patient_name = models.CharField(max_length=100)
    patient_age = models.PositiveIntegerField()
    patient_gender = models.CharField(
        max_length=1, 
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        blank=True, 
        null=True
    )
    patient_phone = models.CharField(max_length=20)
    patient_email = models.EmailField(blank=True, null=True)
    patient_whatsapp = models.CharField(max_length=20, blank=True, null=True)
    
    # Health information
    symptoms = models.TextField(
        blank=True, 
        null=True,
        help_text="Patient symptoms or reason for visit"
    )
    
    present_complaints = models.TextField(
        blank=True, 
        null=True,
        help_text="Current health issues and symptoms"
    )
    
    medical_history = models.TextField(
        blank=True, 
        null=True,
        help_text="Previous medical history"
    )
    
    # Status and payment
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    
    payment_status = models.CharField(
        max_length=20, 
        choices=PAYMENT_STATUS_CHOICES, 
        default='pending'
    )
    
    payment_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=200.00
    )
    
    payment_id = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Razorpay payment ID"
    )
    
    # Admin notes
    admin_notes = models.TextField(
        blank=True, 
        null=True,
        help_text="Internal notes for admin"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ['-created_at']
        # Removed unique_together since appointment_date and appointment_time are now optional
    
    def __str__(self):
        if self.appointment_date:
            return f"{self.patient_name} - {self.service.name} on {self.appointment_date}"
        else:
            return f"{self.patient_name} - {self.service.name} (Date TBD)"
    
    @property
    def is_upcoming(self):
        """Check if the appointment is upcoming"""
        if not self.appointment_date:
            return True  # Consider bookings without dates as upcoming
        return self.appointment_date >= timezone.now().date() and self.status in ['pending', 'confirmed']
    
    @property
    def can_be_cancelled(self):
        """Check if the booking can be cancelled"""
        return self.status in ['pending', 'confirmed'] and self.is_upcoming
    
    def confirm_booking(self):
        """Confirm the booking"""
        self.status = 'confirmed'
        self.confirmed_at = timezone.now()
        self.save()
    
    def complete_booking(self):
        """Mark booking as completed"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()

class PrescriptionUpload(models.Model):
    """
    Prescription and medical report uploads
    """
    booking = models.ForeignKey(
        Booking, 
        on_delete=models.CASCADE, 
        related_name='prescriptions'
    )
    
    patient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='prescriptions'
    )
    
    file = models.FileField(
        upload_to='prescriptions/%Y/%m/%d/',
        help_text="Upload prescription or medical reports (PDF, JPG, PNG)"
    )
    
    file_name = models.CharField(max_length=255, blank=True)
    file_type = models.CharField(max_length=50, blank=True)
    file_size = models.PositiveIntegerField(blank=True, null=True)
    
    description = models.TextField(
        blank=True, 
        null=True,
        help_text="Description of the uploaded file"
    )
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Prescription Upload"
        verbose_name_plural = "Prescription Uploads"
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"Prescription for {self.booking.patient_name} - {self.file_name}"
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file_name = self.file.name
            self.file_size = self.file.size
        super().save(*args, **kwargs)
