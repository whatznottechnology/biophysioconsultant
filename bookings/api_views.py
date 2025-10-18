from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Service, Booking
from .serializers import ServiceSerializer, BookingSerializer
from site_settings.models import PaymentSettings
import razorpay
import time
from datetime import datetime

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API viewset for services
    """
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

class BookingViewSet(viewsets.ModelViewSet):
    """
    API viewset for bookings
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]

class AvailableTimesAPIView(APIView):
    """
    API to get available appointment times for a specific date
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        date_str = request.GET.get('date')
        weekday = request.GET.get('weekday')
        
        if not date_str:
            return Response({
                'error': 'date parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from datetime import time
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
            
            # Get already booked times for this date
            booked_times = Booking.objects.filter(
                appointment_date=date_obj,
                status__in=['pending', 'confirmed']
            ).values_list('appointment_time', flat=True)
            
            available_times = []
            for i, slot_time in enumerate(default_times):
                if slot_time not in booked_times:
                    available_times.append({
                        'id': i + 1,  # Generate ID for frontend compatibility
                        'start_time': slot_time.strftime('%H:%M'),
                        'end_time': (datetime.combine(date_obj, slot_time).replace(minute=slot_time.minute + 30)).time().strftime('%H:%M'),
                        'display_time': slot_time.strftime('%I:%M %p')
                    })
            
            return Response(available_times)
            
        except ValueError:
            return Response({
                'error': 'Invalid date format. Use YYYY-MM-DD'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class CreatePaymentOrderAPIView(APIView):
    """
    API to create Razorpay payment order
    """
    permission_classes = [AllowAny]  # Allow for testing
    
    def post(self, request):
        amount = request.data.get('amount')
        currency = request.data.get('currency', 'INR')
        
        if not amount:
            return Response({
                'success': False,
                'error': 'amount is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Get payment settings from database
            payment_settings = PaymentSettings.get_settings()
            
            if not payment_settings.razorpay_key_id or not payment_settings.razorpay_key_secret:
                return Response({
                    'success': False,
                    'error': 'Payment gateway not configured. Please contact support.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Initialize Razorpay client with settings from database
            client = razorpay.Client(
                auth=(payment_settings.razorpay_key_id, payment_settings.razorpay_key_secret)
            )
            
            # Create Razorpay order
            order_data = {
                'amount': int(float(amount) * 100),  # Amount in paise
                'currency': currency,
                'receipt': f'order_{int(time.time())}',
                'notes': {
                    'service': 'Healthcare Consultation',
                    'patient_name': request.data.get('patient_name', 'Test Patient')
                }
            }
            
            order = client.order.create(data=order_data)
            
            return Response({
                'success': True,
                'order': {
                    'id': order['id'],
                    'amount': order['amount'],
                    'currency': order['currency'],
                    'receipt': order['receipt']
                },
                'razorpay_key': payment_settings.razorpay_key_id
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Payment order creation failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class VerifyPaymentAPIView(APIView):
    """
    API to verify Razorpay payment
    """
    permission_classes = [AllowAny]  # Allow for testing
    
    def post(self, request):
        payment_id = request.data.get('razorpay_payment_id')
        order_id = request.data.get('razorpay_order_id')
        signature = request.data.get('razorpay_signature')
        
        if not all([payment_id, order_id, signature]):
            return Response({
                'success': False,
                'error': 'Missing payment verification data'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Get payment settings from database
            payment_settings = PaymentSettings.get_settings()
            
            if not payment_settings.razorpay_key_id or not payment_settings.razorpay_key_secret:
                return Response({
                    'success': False,
                    'error': 'Payment gateway not configured. Please contact support.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Initialize Razorpay client
            client = razorpay.Client(
                auth=(payment_settings.razorpay_key_id, payment_settings.razorpay_key_secret)
            )
            
            # Verify payment signature
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            
            # This will raise an exception if verification fails
            client.utility.verify_payment_signature(params_dict)
            
            return Response({
                'success': True,
                'message': 'Payment verified successfully',
                'payment_id': payment_id,
                'order_id': order_id
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Payment verification failed: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class RazorpayWebhookView(APIView):
    """
    Webhook handler for Razorpay payment notifications
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            # Get webhook data
            webhook_data = request.data
            event_type = webhook_data.get('event')
            
            # Log webhook data for debugging
            print(f"Razorpay Webhook: {event_type}")
            print(f"Webhook Data: {webhook_data}")
            
            # Get payment settings
            payment_settings = PaymentSettings.get_settings()
            
            # Verify webhook signature (if webhook secret is configured)
            # Note: Razorpay webhook signature verification
            # signature = request.headers.get('X-Razorpay-Signature')
            # if signature and payment_settings.razorpay_webhook_secret:
            #     # Verify signature here
            #     pass
            
            # Handle different webhook events
            if event_type == 'payment.authorized':
                # Payment authorized but not captured yet
                payment_entity = webhook_data.get('payload', {}).get('payment', {}).get('entity', {})
                self._handle_payment_authorized(payment_entity)
                
            elif event_type == 'payment.captured':
                # Payment successfully captured
                payment_entity = webhook_data.get('payload', {}).get('payment', {}).get('entity', {})
                self._handle_payment_captured(payment_entity)
                
            elif event_type == 'payment.failed':
                # Payment failed
                payment_entity = webhook_data.get('payload', {}).get('payment', {}).get('entity', {})
                self._handle_payment_failed(payment_entity)
                
            elif event_type == 'order.paid':
                # Order paid successfully
                order_entity = webhook_data.get('payload', {}).get('order', {}).get('entity', {})
                self._handle_order_paid(order_entity)
            
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"Webhook Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _handle_payment_authorized(self, payment_entity):
        """Handle payment authorized event"""
        payment_id = payment_entity.get('id')
        order_id = payment_entity.get('order_id')
        amount = payment_entity.get('amount', 0) / 100  # Convert from paise to rupees
        
        print(f"Payment Authorized: {payment_id}, Order: {order_id}, Amount: ₹{amount}")
        
        # Update booking if exists
        try:
            booking = Booking.objects.filter(payment_id=payment_id).first()
            if booking:
                booking.payment_status = 'pending'
                booking.save()
                print(f"Booking {booking.booking_id} marked as pending")
        except Exception as e:
            print(f"Error updating booking: {str(e)}")
    
    def _handle_payment_captured(self, payment_entity):
        """Handle payment captured event"""
        payment_id = payment_entity.get('id')
        order_id = payment_entity.get('order_id')
        amount = payment_entity.get('amount', 0) / 100  # Convert from paise to rupees
        
        print(f"Payment Captured: {payment_id}, Order: {order_id}, Amount: ₹{amount}")
        
        # Update booking if exists
        try:
            from django.utils import timezone
            booking = Booking.objects.filter(payment_id=payment_id).first()
            if booking:
                booking.payment_status = 'paid'
                booking.status = 'confirmed'
                booking.confirmed_at = timezone.now()
                booking.save()
                print(f"Booking {booking.booking_id} confirmed with payment")
                
                # Send confirmation email after successful payment
                self._send_booking_confirmation_email(booking)
        except Exception as e:
            print(f"Error updating booking: {str(e)}")
    
    def _send_booking_confirmation_email(self, booking):
        """Send booking confirmation email to patient"""
        try:
            from django.core.mail import send_mail
            from django.template.loader import render_to_string
            from django.conf import settings
            
            subject = f'Booking Confirmation - {booking.booking_id}'
            
            # Prepare context for email template
            context = {
                'booking': booking,
                'site_settings': None,
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
    
    def _handle_payment_failed(self, payment_entity):
        """Handle payment failed event"""
        payment_id = payment_entity.get('id')
        order_id = payment_entity.get('order_id')
        error_code = payment_entity.get('error_code')
        error_description = payment_entity.get('error_description')
        
        print(f"Payment Failed: {payment_id}, Error: {error_code} - {error_description}")
        
        # Update booking if exists
        try:
            booking = Booking.objects.filter(payment_id=payment_id).first()
            if booking:
                booking.payment_status = 'failed'
                booking.admin_notes = f"Payment failed: {error_description}"
                booking.save()
                print(f"Booking {booking.booking_id} marked as failed")
        except Exception as e:
            print(f"Error updating booking: {str(e)}")
    
    def _handle_order_paid(self, order_entity):
        """Handle order paid event"""
        order_id = order_entity.get('id')
        amount = order_entity.get('amount', 0) / 100  # Convert from paise to rupees
        
        print(f"Order Paid: {order_id}, Amount: ₹{amount}")
        
        # This is called when order is fully paid
        # Update all bookings associated with this order
        try:
            from django.utils import timezone
            # In our case, we're using payment_id to track, so this might not be needed
            # But keeping for completeness
            print(f"Order {order_id} marked as paid")
        except Exception as e:
            print(f"Error in order paid handler: {str(e)}")