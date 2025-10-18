from django.views.generic import View, TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.utils import timezone
from .models import Booking, Service
from site_settings.models import PaymentSettings
import razorpay
import uuid


class MultiStepBookingView(View):
    """
    Multi-step booking process for guests

    Steps:
    1. Service Selection
    2. Contact Details
    3. Date & Time Selection
    4. Payment
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
            context['patient_name'] = booking_data.get('patient_name', '')
            context['patient_email'] = booking_data.get('patient_email', '')
            context['patient_phone'] = booking_data.get('patient_phone', '')
            context['patient_whatsapp'] = booking_data.get('patient_whatsapp', '')
            context['patient_age'] = booking_data.get('patient_age', '')
            context['patient_gender'] = booking_data.get('patient_gender', '')

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
            context['appointment_time'] = booking_data.get('appointment_time', '')
            context['present_complaints'] = booking_data.get('present_complaints', '')
            context['medical_history'] = booking_data.get('medical_history', '')

            # Get selected service
            service_id = booking_data.get('service_id')
            if service_id:
                try:
                    context['selected_service'] = Service.objects.get(id=service_id)
                except Service.DoesNotExist:
                    pass

        elif step == '4':
            # Payment step
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
                'patient_whatsapp': booking_data.get('patient_whatsapp'),
                'patient_age': booking_data.get('patient_age'),
                'patient_gender': booking_data.get('patient_gender'),
                'appointment_date': booking_data.get('appointment_date'),
                'appointment_time': booking_data.get('appointment_time'),
                'present_complaints': booking_data.get('present_complaints'),
                'medical_history': booking_data.get('medical_history'),
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
        patient_whatsapp = request.POST.get('patient_whatsapp', '').strip()
        patient_age = request.POST.get('patient_age', '').strip()
        patient_gender = request.POST.get('patient_gender', '').strip()

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
        if not patient_gender:
            errors.append('Gender is required')

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
            'patient_whatsapp': patient_whatsapp,
            'patient_age': patient_age,
            'patient_gender': patient_gender,
        })
        request.session['booking_data'] = booking_data
        request.session.modified = True

        # Move to step 3
        return redirect(f'{reverse("multistep_booking")}?step=3')

    def handle_step3(self, request):
        """Handle date/time and medical details"""
        appointment_date = request.POST.get('appointment_date', '').strip()
        appointment_time = request.POST.get('appointment_time', '').strip()
        present_complaints = request.POST.get('present_complaints', '').strip()
        medical_history = request.POST.get('medical_history', '').strip()

        # Validate required fields
        errors = []
        if not appointment_date:
            errors.append('Appointment date is required')
        if not appointment_time:
            errors.append('Appointment time is required')

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect(f'{reverse("multistep_booking")}?step=3')

        # Store in session
        booking_data = request.session.get('booking_data', {})
        booking_data.update({
            'appointment_date': appointment_date,
            'appointment_time': appointment_time,
            'present_complaints': present_complaints,
            'medical_history': medical_history,
        })
        request.session['booking_data'] = booking_data
        request.session.modified = True

        # Move to step 4 (payment)
        return redirect(f'{reverse("multistep_booking")}?step=4')

    def handle_step4(self, request):
        """Handle payment and create booking"""
        booking_data = request.session.get('booking_data', {})
        payment_method = request.POST.get('payment_method', 'online')

        # Create booking
        try:
            service = Service.objects.get(id=booking_data['service_id'])

            booking = Booking.objects.create(
                service=service,
                patient_name=booking_data.get('patient_name'),
                patient_email=booking_data.get('patient_email'),
                patient_phone=booking_data.get('patient_phone'),
                patient_whatsapp=booking_data.get('patient_whatsapp'),
                patient_age=int(booking_data.get('patient_age', 0)),
                patient_gender=booking_data.get('patient_gender'),
                appointment_date=booking_data.get('appointment_date'),
                appointment_time=booking_data.get('appointment_time'),
                present_complaints=booking_data.get('present_complaints', ''),
                medical_history=booking_data.get('medical_history', ''),
                payment_status='pending' if payment_method == 'online' else 'cash',
                status='pending',
                payment_amount=service.price,
                duration_minutes=service.duration_minutes,
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
                messages.success(request, f'Booking created successfully! Your booking ID is {booking.booking_id}')
                return redirect('thank_you', booking_id=booking.booking_id)

        except Exception as e:
            messages.error(request, f'Booking failed: {str(e)}')
            return redirect(f'{reverse("multistep_booking")}?step=4')
