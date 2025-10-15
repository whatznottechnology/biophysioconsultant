from django.urls import path
from . import views
from .multistep_views import MultiStepBookingView

urlpatterns = [
    # Home and main pages
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('services/', views.ServicesView.as_view(), name='services'),
    
    # Booking URLs
    path('book/', MultiStepBookingView.as_view(), name='multistep_booking'),  # New multistep booking
    path('book-old/', views.BookingCreateView.as_view(), name='book'),  # For backward compatibility
    path('book-appointment/', views.BookingCreateView.as_view(), name='book_appointment'),
    path('booking/create/', views.BookingCreateView.as_view(), name='booking_create'),
    path('book/step/<int:step>/', views.BookingStepView.as_view(), name='booking_step'),
    path('booking/<uuid:booking_id>/', views.BookingDetailView.as_view(), name='booking_detail'),
    path('booking/<uuid:booking_id>/confirm/', views.BookingConfirmView.as_view(), name='booking_confirm'),
    path('booking/<uuid:booking_id>/cancel/', views.BookingCancelView.as_view(), name='booking_cancel'),
    path('booking/success/', views.BookingSuccessView.as_view(), name='booking_success'),
    path('thank-you/<uuid:booking_id>/', views.ThankYouView.as_view(), name='thank_you'),
    
    # User booking URLs
    path('my-bookings/', views.MyBookingsView.as_view(), name='my_bookings'),
    path('bookings/', views.UserBookingsView.as_view(), name='user_bookings'),
    
    # Payment URLs
    path('payment/initiate/', views.PaymentInitiateView.as_view(), name='payment_initiate'),
    path('payment/callback/', views.PaymentCallbackView.as_view(), name='payment_callback'),
    path('payment/success/', views.PaymentSuccessView.as_view(), name='payment_success'),
    path('payment/failed/', views.PaymentFailedView.as_view(), name='payment_failed'),
    
    # Prescription upload
    path('booking/<uuid:booking_id>/upload/', views.PrescriptionUploadView.as_view(), name='prescription_upload'),
    
    # AJAX URLs for dynamic content
    path('ajax/available-times/', views.AvailableTimesView.as_view(), name='available_times'),
    path('ajax/service-details/', views.ServiceDetailsView.as_view(), name='service_details'),
]