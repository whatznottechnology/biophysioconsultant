// Healthcare Booking System JavaScript
document.addEventListener('DOMContentLoaded', function() {
    
    // Mobile menu toggle
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('[role="alert"]');
    messages.forEach(function(message) {
        setTimeout(function() {
            message.style.transition = 'opacity 0.5s ease-out';
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 500);
        }, 5000);
    });
    
    // Loading spinner functions
    window.showLoading = function() {
        const spinner = document.getElementById('loading-spinner');
        if (spinner) {
            spinner.classList.remove('hidden');
        }
    };
    
    window.hideLoading = function() {
        const spinner = document.getElementById('loading-spinner');
        if (spinner) {
            spinner.classList.add('hidden');
        }
    };
    
    // Form validation helper
    window.validateForm = function(formElement) {
        const inputs = formElement.querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;
        
        inputs.forEach(function(input) {
            if (!input.value.trim()) {
                input.classList.add('border-red-500');
                isValid = false;
            } else {
                input.classList.remove('border-red-500');
            }
        });
        
        return isValid;
    };
    
    // Phone number formatting
    window.formatPhoneNumber = function(input) {
        let value = input.value.replace(/\D/g, '');
        if (value.length >= 10) {
            value = value.substring(0, 10);
            value = value.replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3');
        }
        input.value = value;
    };
    
    // Age calculation from date of birth
    window.calculateAge = function(birthDate) {
        const today = new Date();
        const birth = new Date(birthDate);
        let age = today.getFullYear() - birth.getFullYear();
        const monthDiff = today.getMonth() - birth.getMonth();
        
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
            age--;
        }
        
        return age;
    };
    
    // AJAX helper function
    window.makeAjaxRequest = function(url, data, method = 'POST') {
        return fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: method !== 'GET' ? JSON.stringify(data) : null
        })
        .then(response => response.json());
    };
    
    // Get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // PWA Install prompt
    let deferredPrompt;
    
    // Check if app is already installed
    function checkIfInstalled() {
        // Check if app was previously installed
        if (localStorage.getItem('pwaInstalled') === 'true') {
            return true;
        }
        
        // Check if running in standalone mode (installed)
        if (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true) {
            localStorage.setItem('pwaInstalled', 'true');
            return true;
        }
        
        return false;
    }
    
    // Hide install buttons if already installed
    if (checkIfInstalled()) {
        const installButton = document.getElementById('pwa-install-button');
        if (installButton) {
            installButton.classList.add('hidden');
        }
        
        const mobileInstallButton = document.getElementById('mobile-pwa-install-button');
        if (mobileInstallButton) {
            mobileInstallButton.classList.add('hidden');
        }
    }
    
    // Show install button when install prompt is available
    window.addEventListener('beforeinstallprompt', function(e) {
        e.preventDefault();
        deferredPrompt = e;
        
        // Don't show if already installed
        if (checkIfInstalled()) {
            return;
        }
        
        // Show desktop install button
        const installButton = document.getElementById('pwa-install-button');
        if (installButton) {
            installButton.classList.remove('hidden');
            installButton.classList.add('flex');
            
            installButton.addEventListener('click', function() {
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then(function(choiceResult) {
                    if (choiceResult.outcome === 'accepted') {
                        console.log('User accepted the install prompt');
                        localStorage.setItem('pwaInstalled', 'true');
                    } else {
                        console.log('User dismissed the install prompt');
                    }
                    deferredPrompt = null;
                    installButton.classList.remove('flex');
                    installButton.classList.add('hidden');
                });
            });
        }
        
        // Show mobile install button
        const mobileInstallButton = document.getElementById('mobile-pwa-install-button');
        if (mobileInstallButton) {
            mobileInstallButton.classList.remove('hidden');
            mobileInstallButton.classList.add('flex');
            
            mobileInstallButton.addEventListener('click', function() {
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then(function(choiceResult) {
                    if (choiceResult.outcome === 'accepted') {
                        console.log('User accepted the install prompt');
                        localStorage.setItem('pwaInstalled', 'true');
                    } else {
                        console.log('User dismissed the install prompt');
                    }
                    deferredPrompt = null;
                    mobileInstallButton.classList.remove('flex');
                    mobileInstallButton.classList.add('hidden');
                });
            });
        }
    });
    
    // Handle app installed event
    window.addEventListener('appinstalled', function(e) {
        localStorage.setItem('pwaInstalled', 'true');
        
        // Hide desktop button
        const installButton = document.getElementById('pwa-install-button');
        if (installButton) {
            installButton.classList.remove('flex');
            installButton.classList.add('hidden');
        }
        
        // Hide mobile button
        const mobileInstallButton = document.getElementById('mobile-pwa-install-button');
        if (mobileInstallButton) {
            mobileInstallButton.classList.remove('flex');
            mobileInstallButton.classList.add('hidden');
        }
    });
    
    // Service Worker update notification
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.addEventListener('controllerchange', function() {
            window.location.reload();
        });
    }
});

// Booking form specific functions
if (window.location.pathname.includes('/book/')) {
    document.addEventListener('DOMContentLoaded', function() {
        
        // Date picker restrictions
        const dateInput = document.getElementById('appointment_date');
        if (dateInput) {
            // Set minimum date to today
            const today = new Date().toISOString().split('T')[0];
            dateInput.setAttribute('min', today);
            
            // Set maximum date to 30 days from today
            const maxDate = new Date();
            maxDate.setDate(maxDate.getDate() + 30);
            dateInput.setAttribute('max', maxDate.toISOString().split('T')[0]);
        }
        
        // Service selection handler
        const serviceSelect = document.getElementById('service');
        if (serviceSelect) {
            serviceSelect.addEventListener('change', function() {
                const serviceId = this.value;
                if (serviceId) {
                    // Fetch service details via AJAX
                    makeAjaxRequest('/ajax/service-details/', { service_id: serviceId })
                        .then(function(data) {
                            // Update UI with service details
                            updateServiceDetails(data);
                        });
                }
            });
        }
        
        // Date selection handler
        if (dateInput) {
            dateInput.addEventListener('change', function() {
                const selectedDate = this.value;
                const serviceId = document.getElementById('service').value;
                
                if (selectedDate && serviceId) {
                    // Fetch available times
                    makeAjaxRequest('/ajax/available-times/', {
                        date: selectedDate,
                        service_id: serviceId
                    })
                    .then(function(data) {
                        updateAvailableTimes(data.times);
                    });
                }
            });
        }
    });
    
    function updateServiceDetails(data) {
        // Update service price, duration, etc.
        const priceElement = document.getElementById('service-price');
        const durationElement = document.getElementById('service-duration');
        
        if (priceElement) priceElement.textContent = '₹' + data.price;
        if (durationElement) durationElement.textContent = data.duration + ' minutes';
    }
    
    function updateAvailableTimes(times) {
        const timeSelect = document.getElementById('appointment_time');
        if (timeSelect) {
            timeSelect.innerHTML = '<option value="">Select time</option>';
            times.forEach(function(time) {
                const option = document.createElement('option');
                option.value = time.value;
                option.textContent = time.label;
                timeSelect.appendChild(option);
            });
        }
    }
}