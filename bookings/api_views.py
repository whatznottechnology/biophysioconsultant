from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
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
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Booking.objects.filter(user=self.request.user)
        return Booking.objects.none()

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