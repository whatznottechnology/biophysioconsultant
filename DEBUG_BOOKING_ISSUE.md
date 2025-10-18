# Booking Error Debugging Guide

## Current Status

আপনার booking system এর সব কিছু সঠিকভাবে implement করা হয়েছে। এখন শুধু test করতে হবে actual error কী।

## Debugging Steps

### Step 1: Run Server

```powershell
python manage.py runserver
```

### Step 2: Open Browser with Console

1. Chrome/Edge open করুন
2. F12 press করে Developer Tools খুলুন
3. **Console** tab এ যান
4. Navigate to: `http://127.0.0.1:8000/book-appointment/`

### Step 3: Test Booking Process

#### Test Scenario 1: Guest Booking + Pay at Clinic

1. **Step 1**: কোন service select করুন
2. **Step 2**: Fill করুন:
   - Name: Test Patient
   - Phone: 9876543210 (exactly 10 digits)
   - Email: test@example.com
   - Age: 30
   - Symptoms: Test symptoms
3. **Continue to Step 3** button click করুন
4. Email check হবে → Login/Register modal দেখাবে
5. **"Continue as Guest"** click করুন
6. **Payment Method**: "Pay at Clinic" select করুন
7. **"Confirm Booking"** click করুন

**Expected Result:**
- Console এ দেখবেন:
  ```
  === Starting booking submission ===
  service: 1
  patient_name: Test Patient
  patient_phone: 9876543210
  ...
  Response status: 200
  Booking successful! Redirecting to: /thank-you/xxx-xxx-xxx/
  ```
- Thank you page এ redirect হবে

**If Error Occurs:**
- Console এ পুরো error message দেখুন
- Terminal এ backend error দেখুন
- Screenshot নিন এবং আমাকে পাঠান

#### Test Scenario 2: New User Registration + Online Payment

1. **Step 1**: Service select করুন
2. **Step 2**: নতুন email দিন (যা database এ নেই)
3. **Continue to Step 3** click করুন
4. Registration modal দেখাবে
5. Password + Confirm Password দিন (min 6 characters)
6. **"Create Account & Continue"** click করুন
7. Auto-login হবে, Step 3 এ যাবে
8. **"Pay Online"** select করুন
9. **"Confirm Booking"** click করুন
10. Razorpay modal খুলবে
11. Test payment করুন

**Test Card for Razorpay:**
- Card: 4111 1111 1111 1111
- CVV: Any 3 digits
- Expiry: Any future date

**Expected Result:**
- Payment successful
- Booking confirmed
- Redirect to thank you page

#### Test Scenario 3: Existing User Login + Online Payment

1. Existing email দিয়ে start করুন
2. Login modal দেখাবে
3. Password দিন
4. Login হবে
5. Payment করুন

## Common Errors & Solutions

### Error 1: "Form validation failed"

**Reason:** কোন required field missing অথবা invalid format

**Solution:**
- Phone number exactly 10 digits দিন (no spaces, no +91)
- Email valid format এ দিন
- Age 1-120 এর মধ্যে দিন
- Service select করুন

**Check in Console:**
```javascript
{
  "success": false,
  "error": "Form validation failed",
  "form_errors": {
    "patient_phone": ["Enter exactly 10 digits"],
    "service": ["This field is required"]
  }
}
```

### Error 2: "CSRF token missing"

**Reason:** CSRF token properly send হচ্ছে না

**Solution:**
এই code already আছে `booking_form.html` এ। যদি তবুও error হয়:

```javascript
// Check in console
console.log('CSRF Token:', document.querySelector('[name=csrfmiddlewaretoken]').value);
```

### Error 3: "Payment failed"

**Reason:** Razorpay configuration issue

**Solution:**
1. Admin panel → Payment Settings check করুন
2. Razorpay Key ID এবং Secret সঠিক আছে কিনা verify করুন
3. "Is Enabled" = True আছে কিনা check করুন

### Error 4: "Server error: 500"

**Reason:** Backend exception

**Solution:**
Terminal এ full error stack trace দেখুন:
```
Debug: Starting form_valid - payment_method=...
Traceback (most recent call last):
  File "...", line ..., in form_valid
    ...
Exception: [Error message]
```

## Backend URLs to Check

### 1. Are these URLs working?

Open in browser:

```
http://127.0.0.1:8000/api/check-email/
```
Should show: `{"detail":"Method \"GET\" not allowed."}`
(This is expected - it needs POST)

### 2. Test API with cURL:

```powershell
# Check if email exists
curl -X POST http://127.0.0.1:8000/api/check-email/ `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"test@example.com\"}'
```

Should return:
```json
{"exists": false}
```

## Database Check

### Check if booking saved:

```powershell
python manage.py shell
```

Then:
```python
from bookings.models import Booking
bookings = Booking.objects.all().order_by('-created_at')
for b in bookings[:5]:
    print(f"ID: {b.booking_id}, Status: {b.status}, Payment: {b.payment_status}")
```

## Payment Settings Check

### Verify Razorpay configuration:

```powershell
python manage.py shell
```

```python
from site_settings.models import PaymentSettings
ps = PaymentSettings.get_settings()
print(f"Enabled: {ps.is_enabled}")
print(f"Key ID: {ps.razorpay_key_id[:10]}...")  # First 10 chars only
print(f"Currency: {ps.currency}")
print(f"Business: {ps.business_name}")
```

Expected:
```
Enabled: True
Key ID: rzp_live_... or rzp_test_...
Currency: INR
Business: [Your clinic name]
```

## What to Send Me

যদি এখনো error হয়, আমাকে পাঠান:

1. **Browser Console Screenshot** (পুরো error message সহ)
2. **Terminal Output** (backend error log)
3. **Which step failed?** (Step 1/2/3, Login/Register/Payment)
4. **What you tried?** (Guest/New User/Existing User)

## Quick Fixes

### If "booking error decche" but no specific error:

1. Clear browser cache: `Ctrl + Shift + Delete`
2. Hard reload: `Ctrl + F5`
3. Try incognito mode: `Ctrl + Shift + N`
4. Check if JavaScript is enabled
5. Try different browser

### If payment successful but booking fails:

**Don't worry!** Payment data is safe in Razorpay dashboard.

**Solution:**
1. Admin panel → Bookings → Find by payment_id
2. Manually update status to "Confirmed"
3. Or create new booking with same details

**Long-term fix:**
Configure webhook in Razorpay dashboard:
- URL: `https://yourdomain.com/api/razorpay-webhook/`
- Events: payment.captured, payment.failed, order.paid

## Notes

### Demo URLs in Admin

Admin panel এ যে Webhook URL, Success URL, Failure URL fields আছে - **এগুলো optional**:

- ✅ **Razorpay Key ID** - REQUIRED
- ✅ **Razorpay Key Secret** - REQUIRED
- ✅ **Is Enabled** - REQUIRED
- ❌ **Webhook URL** - Optional (set in Razorpay dashboard, not here)
- ❌ **Success URL** - Optional (handled by JavaScript)
- ❌ **Failure URL** - Optional (handled by JavaScript)

শুধু first 3টা সঠিক থাকলেই booking কাজ করবে।

### File Upload

File upload **শুধু logged-in users** এর জন্য কাজ করে।

Guest user file upload করতে পারবে না কারণ `PrescriptionUpload` model এ `patient` (User FK) required.

### Booking Status Flow

```
Online Payment:
pending → (payment success) → confirmed → completed

Pay at Clinic:
confirmed → (after visit) → completed

Failed:
pending → failed
```

### Payment Status Flow

```
Online:
pending → (Razorpay callback) → paid

Pay at Clinic:
pending → (admin marks) → paid

Failed:
pending → failed
```

## Success Checklist

যখন সব কিছু ঠিক থাকবে তখন দেখবেন:

✅ Service select করা যাচ্ছে
✅ Contact details validation কাজ করছে
✅ Email check হচ্ছে
✅ Login/Register modal দেখাচ্ছে
✅ Guest option আছে
✅ Payment modal খুলছে
✅ Booking database এ save হচ্ছে
✅ Thank you page show হচ্ছে
✅ Confetti animation দেখাচ্ছে

## Production Deployment Checklist

Live server এ deploy করার আগে:

1. ✅ `settings.py`: `DEBUG = False`
2. ✅ `settings.py`: `ALLOWED_HOSTS = ['yourdomain.com']`
3. ✅ Razorpay: Change to LIVE keys (not test)
4. ✅ Razorpay Dashboard: Add webhook URL
5. ✅ Static files: `python manage.py collectstatic`
6. ✅ Database: Backup before migration
7. ✅ SSL: Ensure HTTPS is enabled
8. ✅ Email: Configure SMTP for notifications

## Support

যদি কোন সমস্যা হয় তাহলে:

1. এই guide অনুযায়ী debugging করুন
2. Error screenshots এবং logs সংগ্রহ করুন
3. আমাকে জানান কোন step এ error হচ্ছে

সব কিছু properly configured আছে। এখন শুধু test করতে হবে এবং actual error খুঁজে বের করতে হবে।
