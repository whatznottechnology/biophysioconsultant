from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import ContactMessage, ClinicInfo
from .forms import ContactMessageForm

class ContactView(TemplateView):
    """
    Contact page with form and clinic information
    """
    template_name = 'contact/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactMessageForm()
        context['clinic_info'] = ClinicInfo.objects.filter(is_active=True).first()
        return context

class ContactSubmitView(CreateView):
    """
    Handle contact form submission
    """
    model = ContactMessage
    form_class = ContactMessageForm
    template_name = 'contact/contact.html'
    success_url = reverse_lazy('contact:contact')
    
    def form_valid(self, form):
        messages.success(
            self.request, 
            'Thank you for your message. We will get back to you soon!'
        )
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(
            self.request, 
            'Please correct the errors in the form.'
        )
        return render(self.request, self.template_name, {
            'form': form,
            'clinic_info': ClinicInfo.objects.filter(is_active=True).first()
        })

class ClinicInfoView(TemplateView):
    """
    Clinic information page
    """
    template_name = 'contact/clinic_info.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clinic_info'] = ClinicInfo.objects.filter(is_active=True).first()
        return context

class LocationView(TemplateView):
    """
    Clinic location with map
    """
    template_name = 'contact/location.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clinic_info'] = ClinicInfo.objects.filter(is_active=True).first()
        return context

class SendMessageAjaxView(TemplateView):
    """
    AJAX view for sending contact messages
    """
    def post(self, request, *args, **kwargs):
        form = ContactMessageForm(request.POST)
        
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'message': 'Thank you for your message. We will get back to you soon!'
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
