# Healthcare Booking System# Healthcare Booking System for Pratap Bag



A Django-based healthcare booking system that allows guests to book medical appointments online with integrated payment processing and email notifications.A comprehensive Django-based healthcare booking system with PWA support for Mr. Pratap Bag's physiotherapy and alternative medicine practice.



## Features![Django](https://img.shields.io/badge/Django-5.2.7-green)

![Python](https://img.shields.io/badge/Python-3.8+-blue)

- **Guest Booking**: No user registration required - patients can book appointments directly![License](https://img.shields.io/badge/License-MIT-yellow)

- **Service Selection**: Choose from available medical services

- **Payment Integration**: Secure payments via Razorpay## 🏥 About Practitioner

- **Email Notifications**: Automatic booking confirmations sent to patients

- **Prescription Upload**: Patients can upload prescription files during booking**Dr. Pratap Bag**

- **PWA Support**: Progressive Web App features for mobile experience- **Qualifications:** M. D. (Acu.), M. B. S., DMT, DPT, D. Mass. T., D. Cup. T, FWT, PET.

- **REST API**: API endpoints for payment processing and booking management- **Registration:** S/53515/201

- **Responsive Design**: Mobile-friendly interface- **Specialties:** Acupressure, Magnet Therapy, Massage, Cupping, Physiotherapy, Biochemic Consultancy

- **Consultation Fee:** ₹200.00

## Installation

## ✨ Features

### Prerequisites

- Python 3.8+### 🎯 Core Features

- pip- **Mobile-first responsive design** - Optimized for all devices

- Git- **Online appointment booking** with payment integration

- **Simplified user registration** (email + password only)

### Setup Steps- **Guest booking support** for cash payments

- **User dashboard** for booking management

1. **Clone the repository** (if applicable) or navigate to the project directory- **Admin panel** for appointment management

- **PWA capabilities** (offline support, installable)

2. **Create a virtual environment**:

   ```bash### 💳 Payment Integration

   python -m venv venv- **Razorpay payment gateway** for online payments

   venv\Scripts\activate  # On Windows- **Cash payment option** for walk-in appointments

   ```- **Secure payment processing** with callback handling



3. **Install dependencies**:### 📱 PWA Features

   ```bash- **Offline support** through service worker

   pip install -r requirements.txt- **Add to home screen** capability

   ```- **Fast loading** with cached resources

- **Mobile app-like experience**

4. **Configure the database**:

   ```bash### 🏥 Healthcare Specific

   python manage.py migrate- **Service management** with pricing

   ```- **Patient information collection**

- **Symptoms tracking**

5. **Load initial data** (optional):- **Prescription/report upload** system

   ```bash- **Appointment status tracking**

   python manage.py loaddata fixtures/*.json

   ```## 🚀 Quick Start



6. **Configure email settings** in `healthcare_booking/settings.py`:### Prerequisites

   - Update EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD- Python 3.8 or higher

   - Or use environment variables for sensitive data- pip (Python package manager)

- Git (for cloning the repository)

7. **Configure Razorpay** in `healthcare_booking/settings.py`:

   - Set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET### Easy Installation (Windows)

   - Use test keys for development

1. **Clone the repository:**

## Usage   ```bash

   git clone https://github.com/whatznottechnology/physiotherapist_booking.git

### Starting the Server   cd physiotherapist_booking

   ```

Run the development server:

```bash2. **Run the installer:**

python manage.py runserver   ```bash

```   install.bat

   ```

The application will be available at `http://127.0.0.1:8000/`   This will:

   - Create virtual environment

### Booking Process   - Install all dependencies

   - Run database migrations

1. Patients visit the website and select a service   - Create admin user

2. Fill in patient details (name, email, phone, etc.)   - Set up the system

3. Upload prescription files if required

4. Proceed to payment via Razorpay3. **Start the server:**

5. Receive booking confirmation email   ```bash

   start_server.bat

### Admin Panel   ```



Access the Django admin at `http://127.0.0.1:8000/admin/` to:4. **Access the application:**

- Manage services   - Website: http://127.0.0.1:8000

- View bookings   - Admin Panel: http://127.0.0.1:8000/admin

- Configure site settings

- Manage uploaded files### Manual Installation



## API Endpoints1. **Clone and setup:**

   ```bash

- `POST /api/bookings/create/` - Create a new booking   git clone https://github.com/whatznottechnology/physiotherapist_booking.git

- `POST /api/payments/verify/` - Verify payment completion   cd physiotherapist_booking

- `GET /api/services/` - List available services   ```



## Deployment2. **Create virtual environment:**

   ```bash

### Heroku Deployment   python -m venv .venv

   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

1. Install Heroku CLI   ```

2. Login to Heroku: `heroku login`

3. Create app: `heroku create your-app-name`3. **Install dependencies:**

4. Set environment variables:   ```bash

   ```bash   pip install -r requirements.txt

   heroku config:set SECRET_KEY=your-secret-key   ```

   heroku config:set RAZORPAY_KEY_ID=your-razorpay-key-id

   heroku config:set RAZORPAY_KEY_SECRET=your-razorpay-key-secret4. **Environment setup:**

   heroku config:set EMAIL_HOST_USER=your-email@domain.com   ```bash

   heroku config:set EMAIL_HOST_PASSWORD=your-email-password   cp .env.example .env

   ```   # Edit .env file with your settings

5. Deploy: `git push heroku main`   ```



### Local Deployment5. **Database setup:**

   ```bash

Use the provided `start_server.bat` for Windows or configure your preferred WSGI server.   python manage.py migrate

   python manage.py createsuperuser

## Configuration   ```



### Email Settings6. **Run the server:**

Update these in `healthcare_booking/settings.py`:   ```bash

```python   python manage.py runserver

EMAIL_HOST = 'smtp.gmail.com'   ```

EMAIL_PORT = 587

EMAIL_USE_TLS = True## 🛠 Tech Stack

EMAIL_HOST_USER = 'your-email@gmail.com'

EMAIL_HOST_PASSWORD = 'your-app-password'### Backend

```- **Django 5.2.7** - Web framework

- **Django REST Framework** - API development

### Payment Settings- **SQLite** - Database (configurable to PostgreSQL/MySQL)

```python- **Python 3.8+** - Programming language

RAZORPAY_KEY_ID = 'your-razorpay-key-id'

RAZORPAY_KEY_SECRET = 'your-razorpay-key-secret'### Frontend

```- **Django Templates** - Server-side rendering

- **TailwindCSS** - CSS framework

## File Structure- **Alpine.js** - JavaScript framework

- **Font Awesome** - Icons

```

healthcare_booking/### Payment & Services

├── bookings/          # Main booking app- **Razorpay** - Payment gateway

├── blog/             # Blog functionality- **PWA** - Progressive Web App features

├── career/           # Career/job listings- **Service Worker** - Offline capabilities

├── contact/          # Contact forms

├── site_settings/    # Site configuration## 📋 Configuration

├── static/           # Static files

├── templates/        # HTML templates### Environment Variables

├── media/            # Uploaded filesCreate a `.env` file in the root directory:

└── fixtures/         # Initial data

``````env

# Django Settings

## Technologies UsedSECRET_KEY=your-secret-key-here

DEBUG=True

- **Backend**: Django 4.x, Django REST FrameworkALLOWED_HOSTS=localhost,127.0.0.1

- **Database**: SQLite (development), PostgreSQL (production)

- **Payments**: Razorpay# Database (Optional - defaults to SQLite)

- **Email**: SMTPDATABASE_URL=sqlite:///db.sqlite3

- **Frontend**: HTML, CSS, JavaScript, Bootstrap

- **PWA**: Service Worker, Web App Manifest# Razorpay Settings

RAZORPAY_KEY_ID=your-razorpay-key-id

## LicenseRAZORPAY_KEY_SECRET=your-razorpay-key-secret



This project is licensed under the MIT License - see the LICENSE file for details.# Email Settings (Optional)

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend

## SupportEMAIL_HOST=smtp.gmail.com

EMAIL_PORT=587

For issues or questions, please check the existing code or create an issue in the repository.EMAIL_USE_TLS=True
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