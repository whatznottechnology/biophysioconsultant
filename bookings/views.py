from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Service, Booking, PrescriptionUpload
from .forms import BookingForm, PrescriptionUploadForm
from site_settings.models import PaymentSettings
import json
import razorpay

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
        # Check if user wants to pay online and is not logged in
        payment_method = self.request.POST.get('payment_method', 'cash')
        
        print(f"Debug: payment_method={payment_method}")
        print(f"Debug: User authenticated: {self.request.user.is_authenticated}")
        print(f"Debug: POST data: {dict(self.request.POST)}")
        
        if payment_method == 'online' and not self.request.user.is_authenticated:
            # Store form data in session
            self.request.session['booking_form_data'] = {
                'service': form.cleaned_data['service'].id,
                'patient_name': form.cleaned_data['patient_name'],
                'patient_age': form.cleaned_data['patient_age'],
                'patient_phone': form.cleaned_data['patient_phone'],
                'patient_email': form.cleaned_data.get('patient_email', ''),
                'symptoms': form.cleaned_data.get('symptoms', ''),
                'payment_method': payment_method
            }
            
            # Store next URL
            self.request.session['next_url'] = self.request.path
            
            # Return JSON response asking for login/signup
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'requires_login': True,
                    'message': 'Please login or create an account to complete your payment.',
                    'login_url': '/accounts/login/',
                    'register_url': '/accounts/register/'
                })
            else:
                return redirect('/accounts/login/')
        
        try:
            # Handle form submission
            booking = form.save(commit=False)
            
            # Check if payment was already completed (payment_id in POST data)
            payment_id = self.request.POST.get('payment_id')
            
            print(f"Debug: payment_id={payment_id}")
            
            # Set user if authenticated
            if self.request.user.is_authenticated:
                booking.patient = self.request.user
                
                # Update user profile with booking data if not already set
                user = self.request.user
                updated = False
                
                if not user.phone_number and booking.patient_phone:
                    user.phone_number = booking.patient_phone
                    updated = True
                
                if not user.age and booking.patient_age:
                    user.age = booking.patient_age
                    updated = True
                
                # Update name if not set
                if not user.first_name and booking.patient_name:
                    name_parts = booking.patient_name.split(' ', 1)
                    user.first_name = name_parts[0]
                    if len(name_parts) > 1:
                        user.last_name = name_parts[1]
                    updated = True
                
                if updated:
                    user.save()
            
            # Set default values based on payment status
            if payment_id:
                # Payment already completed
                booking.status = 'confirmed'
                booking.payment_status = 'paid'
                booking.payment_id = payment_id
                booking.confirmed_at = timezone.now()
            else:
                # No payment yet
                booking.status = 'pending'
                booking.payment_status = 'pending' if payment_method == 'online' else 'cash'
            
            # Set patient_email from form
            patient_email = form.cleaned_data.get('patient_email')
            if patient_email:
                booking.patient_email = patient_email
            
            # Save the booking
            booking.save()
            
            print(f"Debug: Booking saved successfully with ID: {booking.booking_id}")
            
            # Store booking ID in session
            self.request.session['booking_id'] = str(booking.booking_id)
            
            # Return JSON response for AJAX
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                response_data = {
                    'success': True,
                    'redirect_url': reverse_lazy('thank_you', kwargs={'booking_id': booking.booking_id})
                }
                print(f"Debug: Returning JSON response: {response_data}")
                return JsonResponse(response_data)
            
            return redirect('thank_you', booking_id=booking.booking_id)
            
        except Exception as e:
            print(f"Debug: Error in form_valid: {str(e)}")
            import traceback
            traceback.print_exc()
            
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': f'Booking failed: {str(e)}'
                })
            else:
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
        kwargs['user'] = self.request.user
        return kwargs

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

class BookingDetailView(DetailView):
    """
    Booking details page
    """
    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'
    slug_field = 'booking_id'
    slug_url_kwarg = 'booking_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prescriptions'] = self.object.prescriptions.all()
        return context

class DashboardView(LoginRequiredMixin, TemplateView):
    """
    User dashboard with upcoming appointments and quick actions
    """
    template_name = 'bookings/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user_bookings = Booking.objects.filter(
            patient=self.request.user
        ).order_by('-created_at')
        
        context['upcoming_bookings'] = user_bookings.filter(
            appointment_date__gte=timezone.now().date(),
            status__in=['pending', 'confirmed']
        )[:3]
        
        context['recent_bookings'] = user_bookings[:5]
        context['total_bookings'] = user_bookings.count()
        
        return context

class MyBookingsView(LoginRequiredMixin, ListView):
    """
    List all user bookings
    """
    model = Booking
    template_name = 'bookings/my_bookings.html'
    context_object_name = 'bookings'
    paginate_by = 10
    
    def get_queryset(self):
        return Booking.objects.filter(
            patient=self.request.user
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_bookings = Booking.objects.filter(patient=self.request.user)
        
        # Calculate statistics
        context['total_bookings'] = user_bookings.count()
        context['completed_bookings'] = user_bookings.filter(payment_status='paid').count()
        context['pending_bookings'] = user_bookings.filter(payment_status='pending').count()
        
        # Calculate total spent
        total_spent = sum(booking.payment_amount for booking in user_bookings.filter(payment_status='paid'))
        context['total_spent'] = total_spent
        
        return context

class PaymentInitiateView(TemplateView):
    """
    Initiate Razorpay payment
    """
    template_name = 'bookings/payment_initiate.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        booking_id = self.request.session.get('booking_id')
        if booking_id:
            try:
                booking = Booking.objects.get(booking_id=booking_id)
                context['booking'] = booking
                
                # Get payment settings from database
                payment_settings = PaymentSettings.get_settings()
                
                # Initialize Razorpay client
                if payment_settings.razorpay_key_id and payment_settings.razorpay_key_secret:
                    client = razorpay.Client(
                        auth=(payment_settings.razorpay_key_id, payment_settings.razorpay_key_secret)
                    )
                    
                    # Create Razorpay order
                    order_data = {
                        'amount': int(booking.payment_amount * 100),  # Amount in paise
                        'currency': payment_settings.currency,
                        'receipt': str(booking.booking_id),
                        'notes': {
                            'booking_id': str(booking.booking_id),
                            'patient_name': booking.patient_name,
                            'service': booking.service.name
                        }
                    }
                    
                    order = client.order.create(data=order_data)
                    context['razorpay_order_id'] = order['id']
                    context['razorpay_key'] = payment_settings.razorpay_key_id
                    context['payment_settings'] = payment_settings
                
            except Booking.DoesNotExist:
                messages.error(self.request, 'Booking not found.')
        
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

class BookingConfirmView(DetailView):
    """
    Booking confirmation page
    """
    model = Booking
    template_name = 'bookings/booking_confirm.html'
    context_object_name = 'booking'
    slug_field = 'booking_id'
    slug_url_kwarg = 'booking_id'

class BookingCancelView(DetailView):
    """
    Cancel booking
    """
    model = Booking
    template_name = 'bookings/booking_cancel.html'
    context_object_name = 'booking'
    slug_field = 'booking_id'
    slug_url_kwarg = 'booking_id'
    
    def post(self, request, *args, **kwargs):
        booking = self.get_object()
        
        if booking.can_be_cancelled:
            booking.status = 'cancelled'
            booking.save()
            messages.success(request, 'Booking cancelled successfully.')
        else:
            messages.error(request, 'This booking cannot be cancelled.')
        
        return redirect('my_bookings')

class PrescriptionUploadView(LoginRequiredMixin, CreateView):
    """
    Upload prescription for a booking
    """
    model = PrescriptionUpload
    form_class = PrescriptionUploadForm
    template_name = 'bookings/prescription_upload.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_id = self.kwargs.get('booking_id')
        context['booking'] = get_object_or_404(Booking, booking_id=booking_id)
        return context
    
    def form_valid(self, form):
        booking_id = self.kwargs.get('booking_id')
        booking = get_object_or_404(Booking, booking_id=booking_id)
        
        form.instance.booking = booking
        form.instance.patient = self.request.user
        
        response = super().form_valid(form)
        messages.success(self.request, 'Prescription uploaded successfully.')
        
        return redirect('booking_detail', booking_id=booking_id)

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
                    'description': service.description,
                    'requires_prescription': service.requires_prescription
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


class UserBookingsView(LoginRequiredMixin, ListView):
    """
    User's booking history and management
    """
    model = Booking
    template_name = 'bookings/user_bookings.html'
    context_object_name = 'bookings'
    paginate_by = 10
    
    def get_queryset(self):
        return Booking.objects.filter(
            patient=self.request.user
        ).select_related('service').order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add summary statistics
        user_bookings = self.get_queryset()
        context['total_bookings'] = user_bookings.count()
        context['upcoming_bookings'] = user_bookings.filter(
            status__in=['pending', 'confirmed'],
            appointment_date__gte=timezone.now().date()
        ).count()
        context['completed_bookings'] = user_bookings.filter(
            status='completed'
        ).count()
        
        return context
