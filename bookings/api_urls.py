from django.urls import path
from rest_framework.routers import DefaultRouter
from . import api_views

# API URLs for REST endpoints
app_name = 'bookings_api'

router = DefaultRouter()
router.register(r'services', api_views.ServiceViewSet)
router.register(r'bookings', api_views.BookingViewSet)

urlpatterns = [
    # Custom API endpoints
    path('time-slots/', api_views.AvailableTimesAPIView.as_view(), name='time_slots'),
    path('create-payment-order/', api_views.CreatePaymentOrderAPIView.as_view(), name='create_payment_order'),
    path('verify-payment/', api_views.VerifyPaymentAPIView.as_view(), name='verify_payment'),
] + router.urls