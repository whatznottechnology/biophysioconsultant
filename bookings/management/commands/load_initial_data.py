from django.core.management.base import BaseCommand
from django.utils import timezone
from bookings.models import Service
from site_settings.models import SiteSettings, Testimonial
from contact.models import ClinicInfo

class Command(BaseCommand):
    help = 'Load initial data for the healthcare booking system'

    def handle(self, *args, **options):
        self.stdout.write('Loading initial data...')
        
        # Create site settings
        site_settings, created = SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'Pratap Bag Healthcare',
                'site_tagline': 'Holistic Health & Physiotherapy Services',
                'site_description': 'Professional healthcare services including physiotherapy, acupressure, massage therapy, and alternative medicine by certified practitioner Pratap Bag.',
                'consultation_fee': 200.00,
                'contact_phone': '+91-9876543210',
                'contact_email': 'info@pratapbag.com',
                'contact_address': 'Healthcare Clinic, Medical Street, City - 123456',
                'is_booking_enabled': True,
                'is_payment_enabled': True,
                'booking_advance_days': 30,
                'booking_cancel_hours': 24,
                'admin_email': 'admin@pratapbag.com',
                'pwa_app_name': 'Pratap Bag Healthcare',
                'pwa_short_name': 'PB Healthcare',
                'pwa_theme_color': '#10B981',
                'pwa_background_color': '#ffffff'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Site settings created'))
        else:
            self.stdout.write('✓ Site settings already exist')
        
        # Create services
        services_data = [
            {
                'name': 'Acupressure Therapy',
                'description': 'Traditional acupressure treatment using finger pressure on specific points to promote natural healing and wellness.',
                'duration_minutes': 45,
                'price': 200.00
            },
            {
                'name': 'Magnet Therapy',
                'description': 'Therapeutic use of magnetic fields to stimulate healing and reduce pain and inflammation.',
                'duration_minutes': 30,
                'price': 150.00
            },
            {
                'name': 'Massage Therapy',
                'description': 'Professional therapeutic massage to relieve muscle tension, improve circulation, and promote relaxation.',
                'duration_minutes': 60,
                'price': 300.00
            },
            {
                'name': 'Cupping Therapy',
                'description': 'Traditional cupping technique using suction cups to improve blood circulation and reduce muscle tension.',
                'duration_minutes': 40,
                'price': 250.00
            },
            {
                'name': 'Physiotherapy Session',
                'description': 'Comprehensive physiotherapy assessment and treatment for musculoskeletal conditions and rehabilitation.',
                'duration_minutes': 50,
                'price': 350.00
            },
            {
                'name': 'Biochemic Consultation',
                'description': 'Personalized biochemic salt therapy consultation based on individual health assessment and requirements.',
                'duration_minutes': 30,
                'price': 200.00
            },
            {
                'name': 'Health Wellness Consultation',
                'description': 'Comprehensive health assessment and personalized wellness plan including lifestyle and dietary recommendations.',
                'duration_minutes': 45,
                'price': 400.00
            },
            {
                'name': 'Pain Management Session',
                'description': 'Specialized treatment combining multiple therapies for chronic pain management and relief.',
                'duration_minutes': 60,
                'price': 450.00
            }
        ]
        
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults=service_data
            )
            if created:
                self.stdout.write(f'✓ Service "{service_data["name"]}" created')
        
        # Create clinic info
        clinic_info, created = ClinicInfo.objects.get_or_create(
            name='Pratap Bag Healthcare Clinic',
            defaults={
                'address': 'Medical Complex, Health Street, Downtown',
                'city': 'Wellness City',
                'state': 'Healthcare State',
                'pincode': '123456',
                'country': 'India',
                'phone_primary': '+91-9876543210',
                'email_primary': 'info@pratapbag.com',
                'whatsapp_number': '+91-9876543210',
                'monday_hours': '9:00 AM - 6:00 PM',
                'tuesday_hours': '9:00 AM - 6:00 PM',
                'wednesday_hours': '9:00 AM - 6:00 PM',
                'thursday_hours': '9:00 AM - 6:00 PM',
                'friday_hours': '9:00 AM - 6:00 PM',
                'saturday_hours': '9:00 AM - 6:00 PM',
                'sunday_hours': 'Closed',
                'emergency_contact': '+91-9876543210',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Clinic information created'))
        else:
            self.stdout.write('✓ Clinic information already exists')
        
        # Create sample testimonials
        testimonials_data = [
            {
                'patient_name': 'Rajesh Kumar',
                'patient_location': 'Mumbai',
                'treatment_for': 'Back pain and physiotherapy',
                'testimonial': 'Mr. Pratap Bag\'s treatment was excellent. His acupressure therapy completely relieved my chronic back pain. Highly recommended for anyone looking for natural healing.',
                'rating': 5,
                'is_featured': True,
                'is_approved': True
            },
            {
                'patient_name': 'Priya Sharma',
                'patient_location': 'Delhi',
                'treatment_for': 'Stress and anxiety management',
                'testimonial': 'The holistic approach and personalized care I received was amazing. The massage therapy sessions helped me manage stress better than any medication.',
                'rating': 5,
                'is_featured': True,
                'is_approved': True
            },
            {
                'patient_name': 'Amit Patel',
                'patient_location': 'Pune',
                'treatment_for': 'Sports injury rehabilitation',
                'testimonial': 'As an athlete, I needed specialized care for my injury. The physiotherapy sessions were professional and effective. I recovered faster than expected.',
                'rating': 4,
                'is_featured': True,
                'is_approved': True
            }
        ]
        
        for testimonial_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                patient_name=testimonial_data['patient_name'],
                defaults=testimonial_data
            )
            if created:
                self.stdout.write(f'✓ Testimonial from "{testimonial_data["patient_name"]}" created')
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Initial data loaded successfully!'))
        self.stdout.write('\nYou can now:')
        self.stdout.write('1. Run the development server: python manage.py runserver')
        self.stdout.write('2. Access admin panel: http://127.0.0.1:8000/admin/')
        self.stdout.write('3. Login with: admin / password123')
        self.stdout.write('4. View the website: http://127.0.0.1:8000/')