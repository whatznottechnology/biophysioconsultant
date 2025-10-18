from rest_framework import serializers
from .models import Service, Booking, PrescriptionUpload

class ServiceSerializer(serializers.ModelSerializer):
    """
    Serializer for Service model
    """
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'description', 'duration_minutes', 
            'price', 'created_at'
        ]

class PrescriptionUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for PrescriptionUpload model
    """
    file_size_mb = serializers.SerializerMethodField()
    
    class Meta:
        model = PrescriptionUpload
        fields = [
            'id', 'file', 'file_name', 'file_type', 
            'file_size', 'file_size_mb', 'description', 'uploaded_at'
        ]
    
    def get_file_size_mb(self, obj):
        if obj.file_size:
            return round(obj.file_size / (1024 * 1024), 2)
        return 0

class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for Booking model
    """
    service_name = serializers.CharField(source='service.name', read_only=True)
    service_price = serializers.DecimalField(source='service.price', max_digits=10, decimal_places=2, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    prescriptions = PrescriptionUploadSerializer(many=True, read_only=True)
    is_upcoming = serializers.BooleanField(read_only=True)
    can_be_cancelled = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'service', 'service_name', 'service_price',
            'appointment_date', 'appointment_time', 'duration_minutes',
            'patient_name', 'patient_age', 'patient_gender',
            'patient_phone', 'patient_whatsapp',
            'present_complaints', 'medical_history',
            'status', 'status_display', 'payment_status', 'payment_status_display',
            'payment_amount', 'payment_id',
            'prescriptions', 'is_upcoming', 'can_be_cancelled',
            'created_at', 'updated_at', 'confirmed_at', 'completed_at'
        ]
        read_only_fields = [
            'booking_id', 'status', 'payment_status', 
            'payment_id', 'created_at', 'updated_at', 'confirmed_at', 'completed_at'
        ]
    
    def create(self, validated_data):
        return super().create(validated_data)

class BookingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating bookings with validation
    """
    class Meta:
        model = Booking
        fields = [
            'service', 'appointment_date', 'appointment_time',
            'patient_name', 'patient_age', 'patient_gender',
            'patient_phone', 'patient_whatsapp',
            'present_complaints', 'medical_history'
        ]
    
    def validate(self, data):
        # Check if the time slot is available
        appointment_date = data.get('appointment_date')
        appointment_time = data.get('appointment_time')
        
        if appointment_date and appointment_time:
            existing_booking = Booking.objects.filter(
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status__in=['pending', 'confirmed']
            ).exists()
            
            if existing_booking:
                raise serializers.ValidationError(
                    "This time slot is already booked. Please select a different time."
                )
        
        return data
    
    def create(self, validated_data):
        # Set payment amount from service
        service = validated_data['service']
        validated_data['payment_amount'] = service.price
        validated_data['duration_minutes'] = service.duration_minutes
        
        return super().create(validated_data)