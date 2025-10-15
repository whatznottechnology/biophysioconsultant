from django.core.management.base import BaseCommand
from site_settings.models import PaymentSettings

class Command(BaseCommand):
    help = 'Initialize payment settings with Razorpay test credentials'

    def handle(self, *args, **options):
        # Create or update payment settings
        payment_settings, created = PaymentSettings.objects.get_or_create(
            pk=1,
            defaults={
                'gateway': 'razorpay',
                'is_enabled': True,
                'is_test_mode': True,
                'razorpay_key_id': 'rzp_test_RROBHgb9IrH1w4',
                'razorpay_key_secret': 'hku9Rsre2pbbSeRuP1ALwf4K',
                'currency': 'INR',
                'minimum_amount': 100.00,
                'business_name': 'Pratap Bag Healthcare',
                'enable_netbanking': True,
                'enable_cards': True,
                'enable_wallets': True,
                'enable_upi': True,
                'enable_emi': False,
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created payment settings with Razorpay test credentials')
            )
        else:
            # Update existing settings
            payment_settings.razorpay_key_id = 'rzp_test_RROBHgb9IrH1w4'
            payment_settings.razorpay_key_secret = 'hku9Rsre2pbbSeRuP1ALwf4K'
            payment_settings.is_test_mode = True
            payment_settings.save()
            
            self.stdout.write(
                self.style.SUCCESS('Successfully updated payment settings with Razorpay test credentials')
            )
        
        self.stdout.write(
            self.style.WARNING('Note: These are test credentials. Change them in production!')
        )