from django.views.generic import View, TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.utils import timezone
from .models import Booking, Service
from site_settings.models import PaymentSettings
import razorpay
import uuid

User = get_user_model()


class MultiStepBookingView(View):
    """
    Multi-step booking process with automatic account creation
    
    Steps:
    1. Service Selection
    2. Contact Details
    3. Date & Time Selection
    4. Payment (with password creation for non-logged-in users)
    """
    
    template_name = 'bookings/multistep_booking.html'
    
    def get(self, request):
        """Display the current step of the booking process"""
        step = request.GET.get('step', '1')
        context = self.get_step_context(request, step)
        context['current_step'] = int(step)
        context['total_steps'] = 4
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        """Handle form submissions for each step"""
        step = request.POST.get('step', '1')
        
        if step == '1':
            return self.handle_step1(request)
        elif step == '2':
            return self.handle_step2(request)
        elif step == '3':
            return self.handle_step3(request)
        elif step == '4':
            return self.handle_step4(request)
        
        return redirect('multistep_booking')
    
    def get_step_context(self, request, step):
        """Get context data for each step"""
        context = {}
        
        # Initialize session booking_data if not exists
        if 'booking_data' not in request.session:
            request.session['booking_data'] = {}
        
        booking_data = request.session.get('booking_data', {})
        
        if step == '1':
            # Service selection step
            context['services'] = Service.objects.filter(is_active=True)
            context['selected_service'] = booking_data.get('service_id')
            
        elif step == '2':
            # Contact details step
            if request.user.is_authenticated:
                # Pre-fill from user profile
                context['patient_name'] = request.user.get_full_name() or booking_data.get('patient_name', '')
                context['patient_email'] = request.user.email or booking_data.get('patient_email', '')
                context['patient_phone'] = request.user.phone_number or booking_data.get('patient_phone', '')
                context['patient_age'] = request.user.age or booking_data.get('patient_age', '')
                context['patient_address'] = request.user.address or booking_data.get('patient_address', '')
            else:
                # Use session data
                context['patient_name'] = booking_data.get('patient_name', '')
                context['patient_email'] = booking_data.get('patient_email', '')
                context['patient_phone'] = booking_data.get('patient_phone', '')
                context['patient_age'] = booking_data.get('patient_age', '')
                context['patient_address'] = booking_data.get('patient_address', '')
            
            # Get selected service for display
            service_id = booking_data.get('service_id')
            if service_id:
                try:
                    context['selected_service'] = Service.objects.get(id=service_id)
                except Service.DoesNotExist:
                    pass
                    
        elif step == '3':
            # Date & time selection step
            context['appointment_date'] = booking_data.get('appointment_date', '')
            context['symptoms'] = booking_data.get('symptoms', '')
            
            # Get selected service
            service_id = booking_data.get('service_id')
            if service_id:
                try:
                    context['selected_service'] = Service.objects.get(id=service_id)
                except Service.DoesNotExist:
                    pass
                    
        elif step == '4':
            # Payment step
            context['is_authenticated'] = request.user.is_authenticated
            context['show_password_field'] = not request.user.is_authenticated
            
            # Get selected service and calculate payment
            service_id = booking_data.get('service_id')
            if service_id:
                try:
                    service = Service.objects.get(id=service_id)
                    context['selected_service'] = service
                    context['payment_amount'] = service.price
                except Service.DoesNotExist:
                    pass
            
            # Get payment settings
            context['payment_settings'] = PaymentSettings.get_settings()
            
            # Summary of all entered data
            context['booking_summary'] = {
                'patient_name': booking_data.get('patient_name'),
                'patient_email': booking_data.get('patient_email'),
                'patient_phone': booking_data.get('patient_phone'),
                'patient_age': booking_data.get('patient_age'),
                'appointment_date': booking_data.get('appointment_date'),
                'symptoms': booking_data.get('symptoms'),
            }
        
        return context
    
    def handle_step1(self, request):
        """Handle service selection"""
        service_id = request.POST.get('service')
        
        if not service_id:
            messages.error(request, 'Please select a service')
            return redirect('multistep_booking')
        
        # Validate service exists
        try:
            service = Service.objects.get(id=service_id, is_active=True)
        except Service.DoesNotExist:
            messages.error(request, 'Invalid service selected')
            return redirect('multistep_booking')
        
        # Store in session
        if 'booking_data' not in request.session:
            request.session['booking_data'] = {}
        
        request.session['booking_data']['service_id'] = service_id
        request.session.modified = True
        
        # Move to step 2
        return redirect(f'{reverse("multistep_booking")}?step=2')
    
    def handle_step2(self, request):
        """Handle contact details"""
        # Get form data
        patient_name = request.POST.get('patient_name', '').strip()
        patient_email = request.POST.get('patient_email', '').strip()
        patient_phone = request.POST.get('patient_phone', '').strip()
        patient_age = request.POST.get('patient_age', '').strip()
        patient_address = request.POST.get('patient_address', '').strip()
        
        # Validate required fields
        errors = []
        if not patient_name:
            errors.append('Name is required')
        if not patient_email:
            errors.append('Email is required')
        if not patient_phone:
            errors.append('Phone number is required')
        if not patient_age:
            errors.append('Age is required')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect(f'{reverse("multistep_booking")}?step=2')
        
        # Store in session
        booking_data = request.session.get('booking_data', {})
        booking_data.update({
            'patient_name': patient_name,
            'patient_email': patient_email,
            'patient_phone': patient_phone,
            'patient_age': patient_age,
            'patient_address': patient_address,
        })
        request.session['booking_data'] = booking_data
        request.session.modified = True
        
        # If user is logged in, update profile
        if request.user.is_authenticated:
            user = request.user
            updated = False
            
            if not user.phone_number:
                user.phone_number = patient_phone
                updated = True
            if not user.age:
                user.age = int(patient_age)
                updated = True
            if not user.address:
                user.address = patient_address
                updated = True
            if not user.first_name:
                name_parts = patient_name.split(' ', 1)
                user.first_name = name_parts[0]
                if len(name_parts) > 1:
                    user.last_name = name_parts[1]
                updated = True
            
            if updated:
                user.save()
        
        # Move to step 3
        return redirect(f'{reverse("multistep_booking")}?step=3')
    
    def handle_step3(self, request):
        """Handle date/time and symptoms"""
        appointment_date = request.POST.get('appointment_date', '').strip()
        symptoms = request.POST.get('symptoms', '').strip()
        
        # Store in session
        booking_data = request.session.get('booking_data', {})
        booking_data.update({
            'appointment_date': appointment_date,
            'symptoms': symptoms,
        })
        request.session['booking_data'] = booking_data
        request.session.modified = True
        
        # Move to step 4 (payment)
        return redirect(f'{reverse("multistep_booking")}?step=4')
    
    def handle_step4(self, request):
        """Handle payment and create account if needed"""
        booking_data = request.session.get('booking_data', {})
        payment_method = request.POST.get('payment_method', 'cash')
        
        # If user is not logged in, REQUIRE account creation
        if not request.user.is_authenticated:
            password = request.POST.get('password', '').strip()
            
            # Password is REQUIRED for all bookings
            if not password:
                messages.error(request, 'Please create an account to complete your booking')
                return redirect(f'{reverse("multistep_booking")}?step=4')
            
            # Validate password length
            if len(password) < 8:
                messages.error(request, 'Password must be at least 8 characters long')
                return redirect(f'{reverse("multistep_booking")}?step=4')
            
            # Create user account
            email = booking_data.get('patient_email')
            name = booking_data.get('patient_name', '')
            
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'An account with this email already exists. Please login instead.')
                return redirect(f'{reverse("accounts:login")}?next={reverse("multistep_booking")}%3Fstep=4')
            
            # Generate username from email
            username = email.split('@')[0]
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            # Create user
            name_parts = name.split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=booking_data.get('patient_phone'),
                    age=int(booking_data.get('patient_age', 0)),
                    address=booking_data.get('patient_address'),
                )
                
                # Log the user in
                login(request, user, backend='accounts.backends.EmailOrUsernameBackend')
                messages.success(request, 'Account created successfully! You are now logged in.')
            except Exception as e:
                messages.error(request, f'Account creation failed: {str(e)}')
                return redirect(f'{reverse("multistep_booking")}?step=4')
        
        # At this point, user MUST be authenticated
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to complete booking')
            return redirect(f'{reverse("accounts:login")}?next={reverse("multistep_booking")}%3Fstep=4')
        
        # Create booking
        try:
            service = Service.objects.get(id=booking_data['service_id'])
            
            booking = Booking.objects.create(
                patient=request.user,  # Always associate with user account
                service=service,
                patient_name=booking_data.get('patient_name'),
                patient_age=int(booking_data.get('patient_age', 0)),
                patient_phone=booking_data.get('patient_phone'),
                patient_email=booking_data.get('patient_email'),
                symptoms=booking_data.get('symptoms', ''),
                appointment_date=booking_data.get('appointment_date'),
                payment_status='pending' if payment_method == 'online' else 'cash',
                status='pending',
            )
            
            # Clear booking data from session
            if 'booking_data' in request.session:
                del request.session['booking_data']
            
            # Store booking ID for payment
            request.session['booking_id'] = str(booking.booking_id)
            request.session.modified = True
            
            # Redirect based on payment method
            if payment_method == 'online':
                return redirect('payment_initiate')
            else:
                return redirect('thank_you', booking_id=booking.booking_id)
                
        except Exception as e:
            messages.error(request, f'Booking failed: {str(e)}')
            return redirect(f'{reverse("multistep_booking")}?step=4')
