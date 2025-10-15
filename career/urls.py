from django.urls import path
from . import views

app_name = 'career'

urlpatterns = [
    # Career main page
    path('', views.CareerView.as_view(), name='career'),
    
    # Job application
    path('jobs/<int:pk>/apply/', views.JobApplicationView.as_view(), name='job_apply'),
    path('application/success/', views.ApplicationSuccessView.as_view(), name='application_success'),
    
    # AJAX endpoint for modal form submission
    path('ajax/apply/', views.JobApplicationAjaxView.as_view(), name='job_apply_ajax'),
]