from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, TemplateView, View
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from .models import User
from .forms import CustomUserCreationForm, UserProfileForm

class CustomLoginView(LoginView):
    """
    Custom login view with better styling
    """
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        # Check if there's a next URL in session or GET parameter
        next_url = self.request.session.pop('next_url', None) or self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('accounts:dashboard')
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().get_display_name()}!')
        return super().form_valid(form)

class RegisterView(CreateView):
    """
    User registration view
    """
    model = User
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')  # Redirect to home page after registration
    
    def get_success_url(self):
        # Check if there's a next URL in session or GET parameter  
        next_url = self.request.session.pop('next_url', None) or self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('home')  # Default to home page
    
    def form_valid(self, form):
        # Save the user
        response = super().form_valid(form)
        
        # Log the user in with specific backend
        from django.contrib.auth import get_backends
        backend = get_backends()[0]  # Use the first available backend
        login(self.request, self.object, backend=f'{backend.__module__}.{backend.__class__.__name__}')
        
        messages.success(
            self.request, 
            f'Welcome to Bio-Physio Consultant, {self.object.get_display_name()}! Your account has been created successfully.'
        )
        
        return response
    
    def dispatch(self, request, *args, **kwargs):
        # Redirect if user is already authenticated
        if request.user.is_authenticated:
            return redirect('bookings:dashboard')
        return super().dispatch(request, *args, **kwargs)

class DashboardView(LoginRequiredMixin, TemplateView):
    """
    User dashboard with overview
    """
    template_name = 'accounts/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get user's bookings
        from bookings.models import Booking
        user_bookings = Booking.objects.filter(patient=self.request.user)
        
        context['total_bookings'] = user_bookings.count()
        context['upcoming_bookings'] = user_bookings.filter(
            status__in=['pending', 'confirmed']
        ).count()
        context['completed_bookings'] = user_bookings.filter(
            status='completed'
        ).count()
        context['recent_bookings'] = user_bookings.order_by('-created_at')[:5]
        
        return context

class ProfileView(LoginRequiredMixin, TemplateView):
    """
    User profile view
    """
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get user's bookings
        from bookings.models import Booking
        context['recent_bookings'] = Booking.objects.filter(
            patient=self.request.user
        ).order_by('-created_at')[:5]
        
        return context

class ProfileEditView(LoginRequiredMixin, UpdateView):
    """
    Edit user profile
    """
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated successfully.')
        return super().form_valid(form)

class ChangePasswordView(LoginRequiredMixin, TemplateView):
    """
    Change password view
    """
    template_name = 'accounts/change_password.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PasswordChangeForm(self.request.user)
        return context
    
    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, self.template_name, {'form': form})


class CustomLogoutView(View):
    """
    Custom logout view that handles both GET and POST requests
    """
    
    def get(self, request):
        """Handle GET request - show logout confirmation or directly logout"""
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect('/')
    
    def post(self, request):
        """Handle POST request - logout user"""
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect('/')