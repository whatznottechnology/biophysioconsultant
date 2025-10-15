from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.contrib import messages
from django.http import JsonResponse
from .models import JobOpening, JobApplication
from .forms import JobApplicationForm

class CareerView(TemplateView):
    """
    Main career page with overview and simple application
    """
    template_name = 'career/career.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_openings'] = JobOpening.objects.filter(
            is_active=True
        ).order_by('-created_at')
        return context

class JobApplicationView(CreateView):
    """
    Simplified job application form
    """
    model = JobApplication
    form_class = JobApplicationForm
    template_name = 'career/job_apply.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = get_object_or_404(JobOpening, pk=self.kwargs['pk'], is_active=True)
        return context
    
    def form_valid(self, form):
        job = get_object_or_404(JobOpening, pk=self.kwargs['pk'], is_active=True)
        form.instance.job_opening = job
        
        response = super().form_valid(form)
        
        messages.success(
            self.request,
            'Thank you! Your application has been submitted successfully. We will contact you soon!'
        )
        
        return redirect('career:application_success')

class ApplicationSuccessView(TemplateView):
    """
    Application success/thank you page
    """
    template_name = 'career/application_success.html'

# AJAX Views
class JobApplicationAjaxView(TemplateView):
    """
    AJAX view for job applications
    """
    def post(self, request, *args, **kwargs):
        form = JobApplicationForm(request.POST)
        
        if form.is_valid():
            job_id = request.POST.get('job_id')
            try:
                job = get_object_or_404(JobOpening, pk=job_id, is_active=True)
                
                application = form.save(commit=False)
                application.job_opening = job
                application.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Your application has been submitted successfully! We will contact you soon.',
                    'application_id': application.pk
                })
            except JobOpening.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Job opening not found or no longer active.'
                })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Please check your form data and try again.',
                'errors': form.errors
            })
