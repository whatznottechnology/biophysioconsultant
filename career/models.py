from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

class JobOpening(models.Model):
    """
    Training batches and career opportunities
    """
    JOB_TYPE_CHOICES = [
        ('full_time', 'Exercise Therapy'),
        ('part_time', 'Magnet Therapy'),
        ('contract', 'Massage Therapy'),
        ('internship', 'Physiotherapy'),
        ('volunteer', 'Acupressure'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField(
        help_text="Job requirements and qualifications"
    )
    
    job_type = models.CharField(
        max_length=20, 
        choices=JOB_TYPE_CHOICES, 
        default='full_time',
        verbose_name="Clinical Training"
    )
    
    location = models.CharField(max_length=200)
    salary_min = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True,
        help_text="Minimum tuition fees in INR",
        verbose_name="Tuition Fees (Min)"
    )
    
    salary_max = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True,
        help_text="Maximum tuition fees in INR",
        verbose_name="Tuition Fees (Max)"
    )
    
    is_active = models.BooleanField(default=True)
    application_deadline = models.DateField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "New Batch"
        verbose_name_plural = "New Batches"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def is_deadline_passed(self):
        """Check if application deadline has passed"""
        if self.application_deadline:
            return self.application_deadline < timezone.now().date()
        return False
    
    @property
    def salary_range(self):
        """Return formatted tuition fees range"""
        if self.salary_min and self.salary_max:
            return f"₹{self.salary_min:,.0f} - ₹{self.salary_max:,.0f}"
        elif self.salary_min:
            return f"₹{self.salary_min:,.0f}+"
        return "Tuition fees not specified"

class JobApplication(models.Model):
    """
    Training applications from candidates
    """
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    job_opening = models.ForeignKey(
        JobOpening, 
        on_delete=models.CASCADE, 
        related_name='applications'
    )
    
    # Applicant details
    name = models.CharField(max_length=200, verbose_name="Full Name")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, verbose_name="Sex")
    whatsapp_number = models.CharField(
        validators=[phone_regex], 
        max_length=17,
        verbose_name="WhatsApp No."
    )
    email = models.EmailField(verbose_name="Email")
    qualification = models.CharField(max_length=300, verbose_name="Qualification")
    address = models.TextField(verbose_name="Address")
    
    # Application status
    status = models.CharField(
        max_length=30, 
        choices=STATUS_CHOICES, 
        default='submitted'
    )
    
    admin_notes = models.TextField(
        blank=True, 
        null=True,
        help_text="Internal notes for HR/Admin"
    )
    
    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Training Application"
        verbose_name_plural = "Training Applications"
        ordering = ['-submitted_at']
        unique_together = ['job_opening', 'email']
    
    def __str__(self):
        return f"{self.name} - {self.job_opening.title}"
    
    def mark_as_reviewed(self):
        """Mark application as reviewed"""
        if self.status == 'submitted':
            self.status = 'under_review'
            self.reviewed_at = timezone.now()
            self.save()
