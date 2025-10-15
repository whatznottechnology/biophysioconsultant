from django.core.management.base import BaseCommand
from career.models import JobOpening
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Add demo job openings for testing'

    def handle(self, *args, **options):
        # Clear existing jobs (optional)
        JobOpening.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing job openings'))

        # Job 1: Physiotherapist
        job1 = JobOpening.objects.create(
            title='Physiotherapist',
            description='We are seeking a skilled and compassionate Physiotherapist to join our healthcare team. You will be responsible for assessing, planning, and implementing rehabilitation programs for patients with physical impairments or disabilities.',
            requirements='''• Bachelor's/Master's degree in Physiotherapy
• Valid registration with State Council
• 2+ years of clinical experience
• Knowledge of manual therapy techniques
• Excellent communication and interpersonal skills
• Ability to work independently and as part of a team''',
            location='Kolkata, West Bengal',
            job_type='full_time',
            experience_level='mid',
            salary_min=25000,
            salary_max=40000,
            is_active=True,
            application_deadline=date.today() + timedelta(days=30)
        )
        self.stdout.write(self.style.SUCCESS(f'Created job: {job1.title}'))

        # Job 2: Massage Therapist
        job2 = JobOpening.objects.create(
            title='Massage Therapist',
            description='Join our team as a Massage Therapist and help clients achieve relaxation, pain relief, and improved well-being through therapeutic massage techniques. Experience in various massage modalities is preferred.',
            requirements='''• Certification in Massage Therapy
• Knowledge of different massage techniques (Swedish, Deep Tissue, Sports)
• Good understanding of human anatomy and physiology
• Strong communication skills
• Professional and caring attitude
• Fresh graduates are welcome to apply''',
            location='Kolkata, West Bengal',
            job_type='full_time',
            experience_level='junior',
            salary_min=15000,
            salary_max=25000,
            is_active=True,
            application_deadline=date.today() + timedelta(days=30)
        )
        self.stdout.write(self.style.SUCCESS(f'Created job: {job2.title}'))

        # Job 3: Front Desk Receptionist
        job3 = JobOpening.objects.create(
            title='Front Desk Receptionist',
            description='We are looking for a friendly and organized Front Desk Receptionist to be the first point of contact for our patients. You will handle appointments, patient inquiries, and administrative tasks to ensure smooth clinic operations.',
            requirements='''• High school diploma or equivalent
• Previous experience in healthcare reception is a plus
• Excellent verbal and written communication skills
• Proficiency in MS Office and basic computer skills
• Professional appearance and positive attitude
• Ability to multitask and handle stressful situations
• Knowledge of Bengali and Hindi preferred''',
            location='Kolkata, West Bengal',
            job_type='part_time',
            experience_level='fresher',
            salary_min=10000,
            salary_max=18000,
            is_active=True,
            application_deadline=date.today() + timedelta(days=45)
        )
        self.stdout.write(self.style.SUCCESS(f'Created job: {job3.title}'))

        self.stdout.write(self.style.SUCCESS('\n✅ Successfully added 3 demo job openings!'))
        self.stdout.write(self.style.SUCCESS('Visit /career/ to see them'))
