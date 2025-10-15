from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    # Contact page
    path('', views.ContactView.as_view(), name='contact'),
    path('submit/', views.ContactSubmitView.as_view(), name='contact_submit'),
    
    # Clinic information
    path('clinic-info/', views.ClinicInfoView.as_view(), name='clinic_info'),
    path('location/', views.LocationView.as_view(), name='location'),
    
    # AJAX endpoints
    path('ajax/send-message/', views.SendMessageAjaxView.as_view(), name='send_message_ajax'),
]