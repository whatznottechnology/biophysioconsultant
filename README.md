# Healthcare Booking System for Pratap Bag

A comprehensive Django-based healthcare booking system with PWA support for Mr. Pratap Bag's physiotherapy and alternative medicine practice.

![Django](https://img.shields.io/badge/Django-5.2.7-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🏥 About Practitioner

**Dr. Pratap Bag**
- **Qualifications:** M. D. (Acu.), M. B. S., DMT, DPT, D. Mass. T., D. Cup. T, FWT, PET.
- **Registration:** S/53515/201
- **Specialties:** Acupressure, Magnet Therapy, Massage, Cupping, Physiotherapy, Biochemic Consultancy
- **Consultation Fee:** ₹200.00

## ✨ Features

### 🎯 Core Features
- **Mobile-first responsive design** - Optimized for all devices
- **Online appointment booking** with payment integration
- **Simplified user registration** (email + password only)
- **Guest booking support** for cash payments
- **User dashboard** for booking management
- **Admin panel** for appointment management
- **PWA capabilities** (offline support, installable)

### 💳 Payment Integration
- **Razorpay payment gateway** for online payments
- **Cash payment option** for walk-in appointments
- **Secure payment processing** with callback handling

### 📱 PWA Features
- **Offline support** through service worker
- **Add to home screen** capability
- **Fast loading** with cached resources
- **Mobile app-like experience**

### 🏥 Healthcare Specific
- **Service management** with pricing
- **Patient information collection**
- **Symptoms tracking**
- **Prescription/report upload** system
- **Appointment status tracking**

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)

### Easy Installation (Windows)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/whatznottechnology/physiotherapist_booking.git
   cd physiotherapist_booking
   ```

2. **Run the installer:**
   ```bash
   install.bat
   ```
   This will:
   - Create virtual environment
   - Install all dependencies
   - Run database migrations
   - Create admin user
   - Set up the system

3. **Start the server:**
   ```bash
   start_server.bat
   ```

4. **Access the application:**
   - Website: http://127.0.0.1:8000
   - Admin Panel: http://127.0.0.1:8000/admin

### Manual Installation

1. **Clone and setup:**
   ```bash
   git clone https://github.com/whatznottechnology/physiotherapist_booking.git
   cd physiotherapist_booking
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup:**
   ```bash
   cp .env.example .env
   # Edit .env file with your settings
   ```

5. **Database setup:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run the server:**
   ```bash
   python manage.py runserver
   ```

## 🛠 Tech Stack

### Backend
- **Django 5.2.7** - Web framework
- **Django REST Framework** - API development
- **SQLite** - Database (configurable to PostgreSQL/MySQL)
- **Python 3.8+** - Programming language

### Frontend
- **Django Templates** - Server-side rendering
- **TailwindCSS** - CSS framework
- **Alpine.js** - JavaScript framework
- **Font Awesome** - Icons

### Payment & Services
- **Razorpay** - Payment gateway
- **PWA** - Progressive Web App features
- **Service Worker** - Offline capabilities

## 📋 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Optional - defaults to SQLite)
DATABASE_URL=sqlite:///db.sqlite3

# Razorpay Settings
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret

# Email Settings (Optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Admin Configuration

1. Create superuser: `python manage.py createsuperuser`
2. Login to admin panel: http://127.0.0.1:8000/admin
3. Configure:
   - Services and pricing
   - Time slots
   - Site settings
   - User management

## 📱 Usage

### For Patients
1. **Browse Services** - View available healthcare services
2. **Book Appointment** - Select service and provide details
3. **Choose Payment** - Pay online or choose cash payment
4. **Manage Bookings** - View and track appointments
5. **Upload Documents** - Share prescriptions/reports

### For Admin
1. **Manage Appointments** - View, confirm, modify bookings
2. **Patient Management** - Access patient information
3. **Service Configuration** - Update services and pricing
4. **Reports** - Generate booking and payment reports

## 🔧 Customization

### Adding New Services
```python
# In Django admin or shell
from bookings.models import Service

Service.objects.create(
    name="New Service",
    description="Service description",
    duration_minutes=45,
    price=300.00,
    is_active=True
)
```

### Modifying Booking Flow
- Edit `bookings/views.py` for backend logic
- Modify `templates/bookings/` for frontend templates
- Update `bookings/forms.py` for form validation

## 🚀 Deployment

### Production Setup
1. Set `DEBUG=False` in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Configure domain and SSL
5. Use WSGI server (Gunicorn + Nginx)

### Docker Deployment
```dockerfile
# Dockerfile included for container deployment
docker build -t healthcare-booking .
docker run -p 8000:8000 healthcare-booking
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📞 Support

For support and questions:
- **Email:** support@whatznottechnology.com
- **Issues:** GitHub Issues tab
- **Documentation:** Check the `/docs` folder

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for **Dr. Pratap Bag's Healthcare Practice**
- Developed by **Whatzn** Technology Solutions
- Special thanks to the Django and open-source community

---

**Made with ❤️ for healthcare professionals**