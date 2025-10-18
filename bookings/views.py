from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from .models import Service, Booking, PrescriptionUpload
from .forms import BookingForm
from site_settings.models import PaymentSettings
import json
import razorpay
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

class HomeView(TemplateView):
    """
    Home page view with hero section and key information
    """
    template_name = 'bookings/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get featured services (limit to 6)
        context['featured_services'] = Service.objects.filter(
            is_active=True
        ).order_by('name')[:6]
        
        # Get recent testimonials if available
        from site_settings.models import Testimonial
        context['testimonials'] = Testimonial.objects.filter(
            is_approved=True,
            is_featured=True
        ).order_by('-created_at')[:3]
        
        return context

class AboutView(TemplateView):
    """
    About page with practitioner information
    """
    template_name = 'bookings/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context

class ServicesView(ListView):
    """
    Services listing page
    """
    model = Service
    template_name = 'bookings/services.html'
    context_object_name = 'services'
    queryset = Service.objects.filter(is_active=True).order_by('name')

@method_decorator(ensure_csrf_cookie, name='dispatch')
class BookingCreateView(CreateView):
    """
    Simplified booking form (no login required until payment)
    """
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(is_active=True)
        return context
    
    def dispatch(self, request, *args, **kwargs):
        """Wrap dispatch to catch any unexpected errors for AJAX requests"""
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            print(f"Debug: Unexpected error in dispatch: {str(e)}")
            import traceback
            traceback.print_exc()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': f'Server error: {str(e)}'
                })
            raise
    
    def form_invalid(self, form):
        """Handle form validation errors for AJAX requests"""
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Return JSON response with form errors
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = [str(error) for error in error_list]
            
            return JsonResponse({
                'success': False,
                'error': 'Form validation failed',
                'form_errors': errors
            })
        
        return super().form_invalid(form)
    
    def form_valid(self, form):
        try:
            # Get payment method
            payment_method = self.request.POST.get('payment_method', 'cash')
            payment_id = self.request.POST.get('payment_id', '')
            
            print(f"Debug: Starting form_valid - payment_method={payment_method}, payment_id={payment_id}")
            
            # Create booking instance
            booking = form.save(commit=False)
            
            # Set payment status based on payment method and payment_id
            if payment_id:
                # Online payment completed
                booking.status = 'confirmed'
                booking.payment_status = 'paid'
                booking.payment_id = payment_id
                booking.confirmed_at = timezone.now()
                print(f"Debug: Payment completed - payment_id={payment_id}")
            elif payment_method == 'online':
                # Online payment selected but not completed yet
                booking.status = 'pending'
                booking.payment_status = 'pending'
                print(f"Debug: Online payment pending")
            else:
                # Pay at clinic
                booking.status = 'confirmed'
                booking.payment_status = 'pending'
                booking.confirmed_at = timezone.now()
                print(f"Debug: Pay at clinic selected")
            
            # Set patient email from form
            if form.cleaned_data.get('patient_email'):
                booking.patient_email = form.cleaned_data['patient_email']
            
            # Handle file upload
            prescription_file = self.request.FILES.get('prescription_file')
            if prescription_file:
                print(f"Debug: File uploaded: {prescription_file.name}")
                # File will be handled after booking is saved
            
            # Save the booking
            booking.save()
            print(f"Debug: Booking saved successfully - ID: {booking.booking_id}")
            
            # Handle prescription file upload if provided
            if prescription_file:
                from .models import PrescriptionUpload
                prescription = PrescriptionUpload.objects.create(
                    booking=booking,
                    file=prescription_file,
                    description='Uploaded during booking'
                )
                print(f"Debug: Prescription uploaded: {prescription.id}")
            
            # Send booking confirmation email
            self.send_booking_confirmation_email(booking)
            
            # Return JSON response for AJAX
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                response_data = {
                    'success': True,
                    'message': 'Booking created successfully',
                    'booking_id': str(booking.booking_id),
                    'redirect_url': f'/thank-you/{booking.booking_id}/'
                }
                print(f"Debug: Returning JSON response: {response_data}")
                return JsonResponse(response_data)
            
            # Redirect to thank you page
            return redirect('thank_you', booking_id=booking.booking_id)
            
        except Exception as e:
            print(f"Debug: Error in form_valid: {str(e)}")
            import traceback
            traceback.print_exc()
            
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': f'Booking failed: {str(e)}'
                }, status=500)
            else:
                messages.error(self.request, f'Booking failed: {str(e)}')
                return self.form_invalid(form)
    
    def get_initial(self):
        initial = super().get_initial()
        
        # Restore form data from session if available
        if 'booking_form_data' in self.request.session:
            form_data = self.request.session.pop('booking_form_data')
            initial.update(form_data)
            
            # Convert service ID back to Service object
            if 'service' in form_data:
                try:
                    initial['service'] = Service.objects.get(id=form_data['service'])
                except Service.DoesNotExist:
                    pass
        
        return initial
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs
    
    def send_booking_confirmation_email(self, booking):
        """
        Send booking confirmation email to patient
        """
        try:
            subject = f'Booking Confirmation - {booking.booking_id}'
            
            # Prepare context for email template
            context = {
                'booking': booking,
                'site_settings': None,  # We'll get this from database if needed
            }
            
            # Try to get site settings
            try:
                from site_settings.models import SiteSettings
                context['site_settings'] = SiteSettings.get_settings()
            except:
                pass
            
            # Render email content
            html_message = render_to_string('emails/booking_confirmation.html', context)
            plain_message = render_to_string('emails/booking_confirmation.txt', context)
            
            # Send email
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.patient_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            print(f"Booking confirmation email sent to {booking.patient_email} for booking {booking.booking_id}")
            return True
            
        except Exception as e:
            print(f"Failed to send booking confirmation email: {str(e)}")
            return False

class ThankYouView(TemplateView):
    """
    Thank you page after successful booking
    """
    template_name = 'bookings/thank_you.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get booking by ID from URL
        booking_id = kwargs.get('booking_id')
        if booking_id:
            try:
                booking = Booking.objects.get(booking_id=booking_id)
                context['booking'] = booking
            except Booking.DoesNotExist:
                context['booking'] = None
        
        return context

class BookingStepView(TemplateView):
    """
    Individual steps in booking process
    """
    template_name = 'bookings/booking_step.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step'] = kwargs.get('step', 1)
        context['services'] = Service.objects.filter(is_active=True)
        return context

class PaymentCallbackView(TemplateView):
    """
    Handle Razorpay payment callback
    """
    template_name = 'bookings/payment_callback.html'
    
    def post(self, request, *args, **kwargs):
        # Handle payment verification
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')
        
        if payment_id and order_id and signature:
            try:
                # Get payment settings from database
                payment_settings = PaymentSettings.get_settings()
                
                # Verify payment signature
                client = razorpay.Client(
                    auth=(payment_settings.razorpay_key_id, payment_settings.razorpay_key_secret)
                )
                
                client.utility.verify_payment_signature({
                    'razorpay_order_id': order_id,
                    'razorpay_payment_id': payment_id,
                    'razorpay_signature': signature
                })
                
                # Update booking payment status
                booking_id = request.session.get('booking_id')
                if booking_id:
                    booking = Booking.objects.get(booking_id=booking_id)
                    booking.payment_status = 'paid'
                    booking.payment_id = payment_id
                    booking.confirm_booking()
                    
                    # Clear booking ID from session
                    del request.session['booking_id']
                    
                    messages.success(request, 'Payment successful! Your booking is confirmed.')
                    return redirect('payment_success')
                
            except Exception as e:
                messages.error(request, 'Payment verification failed.')
                return redirect('payment_failed')
        
        return redirect('payment_failed')

class PaymentSuccessView(TemplateView):
    """
    Payment success page
    """
    template_name = 'bookings/payment_success.html'

class PaymentFailedView(TemplateView):
    """
    Payment failed page
    """
    template_name = 'bookings/payment_failed.html'

# AJAX Views
class AvailableTimesView(TemplateView):
    """
    AJAX view to get available appointment times
    """
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        date_str = data.get('date')
        service_id = data.get('service_id')
        
        if date_str and service_id:
            from datetime import datetime, time
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            # Define default time slots (9 AM to 6 PM, excluding lunch 1-2 PM)
            default_times = [
                time(9, 0),   # 9:00 AM
                time(9, 30),  # 9:30 AM
                time(10, 0),  # 10:00 AM
                time(10, 30), # 10:30 AM
                time(11, 0),  # 11:00 AM
                time(11, 30), # 11:30 AM
                time(12, 0),  # 12:00 PM
                time(12, 30), # 12:30 PM
                time(14, 0),  # 2:00 PM
                time(14, 30), # 2:30 PM
                time(15, 0),  # 3:00 PM
                time(15, 30), # 3:30 PM
                time(16, 0),  # 4:00 PM
                time(16, 30), # 4:30 PM
                time(17, 0),  # 5:00 PM
                time(17, 30), # 5:30 PM
            ]
            
            # Check for existing bookings
            booked_times = Booking.objects.filter(
                appointment_date=date_obj,
                status__in=['pending', 'confirmed']
            ).values_list('appointment_time', flat=True)
            
            available_times = []
            for slot_time in default_times:
                if slot_time not in booked_times:
                    available_times.append({
                        'value': slot_time.strftime('%H:%M'),
                        'label': slot_time.strftime('%I:%M %p')
                    })
            
            return JsonResponse({'times': available_times})
        
        return JsonResponse({'times': []})

class ServiceDetailsView(TemplateView):
    """
    AJAX view to get service details
    """
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        service_id = data.get('service_id')
        
        if service_id:
            try:
                service = Service.objects.get(id=service_id, is_active=True)
                return JsonResponse({
                    'price': float(service.price),
                    'duration': service.duration_minutes,
                    'description': service.description
                })
            except Service.DoesNotExist:
                pass
        
        return JsonResponse({'error': 'Service not found'})


class BookingSuccessView(TemplateView):
    """
    Booking success page
    """
    template_name = 'bookings/booking_success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get booking from session or URL parameter
        booking_id = self.request.GET.get('booking_id')
        if booking_id:
            try:
                booking = Booking.objects.get(booking_id=booking_id)
                context['booking'] = booking
            except Booking.DoesNotExist:
                context['booking'] = None
        
        # Get clinic info
        from contact.models import ClinicInfo
        try:
            context['clinic_info'] = ClinicInfo.objects.filter(is_active=True).first()
        except:
            context['clinic_info'] = None
        
        return context



