from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from career.models import JobOpening, JobApplication, TrainingProgram, TrainingEnrollment
import random


class Command(BaseCommand):
    help = 'Create sample career data including job openings, training programs, and applications'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample career data...')
        
        # Clear existing data
        JobApplication.objects.all().delete()
        JobOpening.objects.all().delete()
        TrainingEnrollment.objects.all().delete()
        TrainingProgram.objects.all().delete()
        
        # Create Job Openings
        job_openings_data = [
            {
                'title': 'Senior Physiotherapist',
                'description': 'We are seeking an experienced physiotherapist to join our healthcare team. The ideal candidate will have expertise in manual therapy, exercise prescription, and patient rehabilitation.',
                'requirements': """
• Bachelor's or Master's degree in Physiotherapy
• Valid license to practice physiotherapy
• Minimum 3-5 years of clinical experience
• Experience with orthopedic and neurological conditions
• Excellent communication and interpersonal skills
• Knowledge of modern rehabilitation techniques
• Proficiency in assessment and treatment planning
                """.strip(),
                'job_type': 'full_time',
                'experience_level': 'senior',
                'location': 'Kolkata, West Bengal',
                'salary_min': 45000,
                'salary_max': 65000,
                'application_deadline': date.today() + timedelta(days=30),
            },
            {
                'title': 'Junior Acupuncturist',
                'description': 'Join our alternative medicine team as a junior acupuncturist. This position offers excellent growth opportunities and hands-on training with experienced practitioners.',
                'requirements': """
• Diploma/Certification in Acupuncture
• Basic knowledge of Traditional Chinese Medicine
• Understanding of anatomy and physiology
• Fresh graduates are welcome to apply
• Willingness to learn and adapt
• Good manual dexterity and attention to detail
• Patient and empathetic approach
                """.strip(),
                'job_type': 'full_time',
                'experience_level': 'junior',
                'location': 'Kolkata, West Bengal',
                'salary_min': 25000,
                'salary_max': 35000,
                'application_deadline': date.today() + timedelta(days=45),
            },
            {
                'title': 'Massage Therapist',
                'description': 'We are looking for a skilled massage therapist to provide therapeutic massage services to our patients. Experience in various massage techniques is preferred.',
                'requirements': """
• Certification in Massage Therapy
• Knowledge of various massage techniques (Swedish, Deep tissue, Therapeutic)
• Understanding of anatomy and muscle groups
• 1-2 years of experience preferred
• Physical stamina and strength
• Professional demeanor and communication skills
• Ability to work with diverse patient populations
                """.strip(),
                'job_type': 'part_time',
                'experience_level': 'junior',
                'location': 'Kolkata, West Bengal',
                'salary_min': 20000,
                'salary_max': 30000,
                'application_deadline': date.today() + timedelta(days=20),
            },
            {
                'title': 'Healthcare Assistant',
                'description': 'Entry-level position for someone passionate about healthcare. This role involves supporting our medical staff and assisting with patient care activities.',
                'requirements': """
• High school diploma or equivalent
• Basic knowledge of healthcare procedures
• Excellent communication skills
• Compassionate and caring nature
• Ability to work in a team environment
• Basic computer skills
• Willingness to learn and follow protocols
• Physical ability to assist patients
                """.strip(),
                'job_type': 'full_time',
                'experience_level': 'fresher',
                'location': 'Kolkata, West Bengal',
                'salary_min': 18000,
                'salary_max': 25000,
                'application_deadline': date.today() + timedelta(days=25),
            },
            {
                'title': 'Yoga Instructor Intern',
                'description': 'Internship opportunity for aspiring yoga instructors. Gain hands-on experience in our wellness center while learning from experienced practitioners.',
                'requirements': """
• Yoga certification from recognized institute
• Basic knowledge of yoga asanas and breathing techniques
• Enthusiastic and dedicated personality
• Good physical fitness
• Ability to demonstrate yoga poses
• Communication skills for group instruction
• Flexible schedule availability
                """.strip(),
                'job_type': 'internship',
                'experience_level': 'fresher',
                'location': 'Kolkata, West Bengal',
                'salary_min': 10000,
                'salary_max': 15000,
                'application_deadline': date.today() + timedelta(days=15),
            },
            {
                'title': 'Ayurvedic Consultant',
                'description': 'Experienced Ayurvedic practitioner needed to provide consultation and treatment planning for patients seeking alternative medicine solutions.',
                'requirements': """
• BAMS degree or equivalent Ayurvedic qualification
• Valid registration with Ayurvedic council
• Minimum 5 years of clinical experience
• Knowledge of Panchakarma and Ayurvedic treatments
• Excellent diagnostic skills
• Experience in pulse diagnosis and constitutional analysis
• Strong knowledge of herbal medicines and preparations
                """.strip(),
                'job_type': 'contract',
                'experience_level': 'senior',
                'location': 'Kolkata, West Bengal',
                'salary_min': 50000,
                'salary_max': 75000,
                'application_deadline': date.today() + timedelta(days=35),
            },
        ]
        
        job_openings = []
        for job_data in job_openings_data:
            job = JobOpening.objects.create(**job_data)
            job_openings.append(job)
            self.stdout.write(f'Created job opening: {job.title}')
        
        # Create Training Programs
        training_programs_data = [
            {
                'title': 'Certified Acupressure Therapist Program',
                'description': 'Comprehensive training program in acupressure therapy covering traditional techniques, anatomy, and practical applications.',
                'detailed_curriculum': """
Module 1: Introduction to Acupressure (Week 1-2)
• History and principles of acupressure
• Understanding energy meridians and pressure points
• Basic anatomy and physiology

Module 2: Acupressure Techniques (Week 3-4)
• Hand positions and pressure application
• Common acupressure points and their benefits
• Safety precautions and contraindications

Module 3: Practical Applications (Week 5-6)
• Treatment protocols for common conditions
• Hands-on practice sessions
• Case studies and patient assessment

Module 4: Advanced Techniques (Week 7-8)
• Specialized acupressure methods
• Integration with other therapies
• Professional practice and ethics

Final Assessment and Certification
                """.strip(),
                'program_type': 'certification',
                'level': 'intermediate',
                'duration_hours': 120,
                'duration_weeks': 8,
                'fee': 25000,
                'max_participants': 15,
                'prerequisites': 'Basic understanding of anatomy or healthcare background preferred',
                'registration_deadline': date.today() + timedelta(days=20),
                'start_date': date.today() + timedelta(days=30),
                'end_date': date.today() + timedelta(days=86),
            },
            {
                'title': 'Basic Physiotherapy Workshop',
                'description': 'Intensive 2-day workshop covering fundamental physiotherapy techniques and assessment methods.',
                'detailed_curriculum': """
Day 1: Assessment and Evaluation
• Patient history taking and physical examination
• Range of motion assessment
• Muscle strength testing
• Postural analysis and gait assessment

Day 2: Treatment Techniques
• Manual therapy techniques
• Exercise prescription and progression
• Electrotherapy modalities
• Home exercise program design

Practical Sessions:
• Hands-on practice with real case scenarios
• Peer assessment and feedback
• Equipment demonstration and usage
                """.strip(),
                'program_type': 'workshop',
                'level': 'beginner',
                'duration_hours': 16,
                'duration_weeks': 1,
                'fee': 8000,
                'max_participants': 20,
                'prerequisites': 'Healthcare students or professionals',
                'registration_deadline': date.today() + timedelta(days=15),
                'start_date': date.today() + timedelta(days=25),
                'end_date': date.today() + timedelta(days=26),
            },
            {
                'title': 'Advanced Cupping Therapy Certification',
                'description': 'Advanced certification program in cupping therapy including traditional and modern techniques.',
                'detailed_curriculum': """
Week 1: Foundations of Cupping
• History and cultural background
• Types of cupping (dry, wet, fire, suction)
• Anatomy and meridian theory
• Safety protocols and sterilization

Week 2: Practical Techniques
• Cup selection and preparation
• Application techniques for different conditions
• Pressure adjustment and timing
• Post-treatment care and advice

Week 3: Clinical Applications
• Treatment protocols for specific conditions
• Combination with other therapies
• Patient assessment and contraindications
• Case study analysis

Week 4: Advanced Practice
• Complex cupping techniques
• Business aspects of cupping practice
• Legal and ethical considerations
• Final practical examination
                """.strip(),
                'program_type': 'certification',
                'level': 'advanced',
                'duration_hours': 80,
                'duration_weeks': 4,
                'fee': 18000,
                'max_participants': 12,
                'prerequisites': 'Basic knowledge of traditional medicine or completed basic cupping course',
                'registration_deadline': date.today() + timedelta(days=25),
                'start_date': date.today() + timedelta(days=40),
                'end_date': date.today() + timedelta(days=68),
            },
            {
                'title': 'Magnet Therapy Practitioner Course',
                'description': 'Learn the therapeutic applications of magnetic field therapy for pain management and healing.',
                'detailed_curriculum': """
Module 1: Introduction to Magnet Therapy
• Scientific basis of magnetic therapy
• Types of magnets and their properties
• Biological effects of magnetic fields
• Historical overview and modern applications

Module 2: Practical Applications
• Magnet placement techniques
• Treatment duration and intensity
• Safety guidelines and contraindications
• Equipment selection and maintenance

Module 3: Clinical Practice
• Treatment protocols for common conditions
• Pain management applications
• Combining with other therapies
• Patient education and counseling

Module 4: Professional Development
• Setting up magnet therapy practice
• Documentation and record keeping
• Continuing education requirements
• Certification examination
                """.strip(),
                'program_type': 'certification',
                'level': 'intermediate',
                'duration_hours': 60,
                'duration_weeks': 6,
                'fee': 15000,
                'max_participants': 18,
                'prerequisites': 'Healthcare background or completion of basic therapy course',
                'registration_deadline': date.today() + timedelta(days=18),
                'start_date': date.today() + timedelta(days=35),
                'end_date': date.today() + timedelta(days=77),
            },
            {
                'title': 'Online Biochemic Medicine Seminar',
                'description': 'Virtual seminar series on biochemic medicine principles and applications in modern healthcare.',
                'detailed_curriculum': """
Session 1: Fundamentals of Biochemic Medicine
• Dr. Schuessler's cell salt theory
• 12 essential tissue salts and their functions
• Principles of deficiency and supplementation
• Integration with conventional medicine

Session 2: Diagnostic Methods
• Constitutional analysis
• Symptom mapping to tissue salts
• Facial diagnosis techniques
• Case history taking methods

Session 3: Treatment Protocols
• Dosage and potency selection
• Combination remedies and their uses
• Treatment duration and monitoring
• Managing acute and chronic conditions

Session 4: Advanced Applications
• Pediatric biochemic medicine
• Geriatric applications
• Sports medicine and tissue salts
• Future trends and research
                """.strip(),
                'program_type': 'online',
                'level': 'intermediate',
                'duration_hours': 24,
                'duration_weeks': 4,
                'fee': 12000,
                'max_participants': 50,
                'prerequisites': 'Basic knowledge of homeopathy or alternative medicine',
                'registration_deadline': date.today() + timedelta(days=12),
                'start_date': date.today() + timedelta(days=22),
                'end_date': date.today() + timedelta(days=50),
            },
        ]
        
        training_programs = []
        for program_data in training_programs_data:
            program = TrainingProgram.objects.create(**program_data)
            training_programs.append(program)
            self.stdout.write(f'Created training program: {program.title}')
        
        # Create sample job applications
        sample_applicants = [
            {
                'first_name': 'Priya',
                'last_name': 'Sharma',
                'email': 'priya.sharma@email.com',
                'phone': '+919876543210',
                'current_location': 'Kolkata, West Bengal',
                'total_experience_years': 4,
                'current_salary': 35000,
                'expected_salary': 50000,
                'notice_period_days': 30,
                'cover_letter': 'I am excited to apply for this position as it aligns perfectly with my career goals in physiotherapy.',
                'portfolio_url': 'https://linkedin.com/in/priyasharma',
                'status': 'under_review',
            },
            {
                'first_name': 'Rahul',
                'last_name': 'Das',
                'email': 'rahul.das@email.com',
                'phone': '+919876543211',
                'current_location': 'Howrah, West Bengal',
                'total_experience_years': 1,
                'current_salary': 20000,
                'expected_salary': 28000,
                'notice_period_days': 15,
                'cover_letter': 'As a recent graduate in physiotherapy, I am eager to contribute to your team and gain valuable experience.',
                'status': 'submitted',
            },
            {
                'first_name': 'Sneha',
                'last_name': 'Roy',
                'email': 'sneha.roy@email.com',
                'phone': '+919876543212',
                'current_location': 'Salt Lake, Kolkata',
                'total_experience_years': 0,
                'expected_salary': 22000,
                'notice_period_days': 0,
                'cover_letter': 'I am passionate about alternative medicine and would love to start my career with your esteemed organization.',
                'status': 'shortlisted',
            },
        ]
        
        # Assign applications to random job openings
        for i, applicant_data in enumerate(sample_applicants):
            job = random.choice(job_openings)
            applicant_data['job_opening'] = job
            # Create a dummy resume path (in real scenario, this would be an actual file)
            applicant_data['resume'] = f'resumes/2024/10/09/resume_{i+1}.pdf'
            
            application = JobApplication.objects.create(**applicant_data)
            self.stdout.write(f'Created job application: {application.full_name} for {job.title}')
        
        # Create sample training enrollments
        sample_enrollees = [
            {
                'first_name': 'Amit',
                'last_name': 'Kumar',
                'email': 'amit.kumar@email.com',
                'phone': '+919876543213',
                'qualification': 'BHMS, Certified Yoga Instructor',
                'experience': '2 years in holistic wellness center',
                'motivation': 'I want to expand my skills in acupressure to provide better treatment to my patients.',
                'status': 'enrolled',
                'payment_status': 'paid',
            },
            {
                'first_name': 'Ritu',
                'last_name': 'Sen',
                'email': 'ritu.sen@email.com',
                'phone': '+919876543214',
                'qualification': 'BPT, Diploma in Naturopathy',
                'experience': '3 years in physiotherapy clinic',
                'motivation': 'Looking to learn advanced cupping techniques to enhance my practice.',
                'status': 'enrolled',
                'payment_status': 'paid',
            },
            {
                'first_name': 'Soumitra',
                'last_name': 'Ghosh',
                'email': 'soumitra.ghosh@email.com',
                'phone': '+919876543215',
                'qualification': 'MSc in Sports Medicine',
                'experience': 'Fresh graduate seeking practical training',
                'motivation': 'Interested in learning physiotherapy techniques for sports injury management.',
                'status': 'pending',
                'payment_status': 'pending',
            },
        ]
        
        # Assign enrollments to random training programs
        for i, enrollee_data in enumerate(sample_enrollees):
            program = random.choice(training_programs)
            enrollee_data['program'] = program
            if enrollee_data['payment_status'] == 'paid':
                enrollee_data['payment_amount'] = program.fee
            else:
                enrollee_data['payment_amount'] = 0
            
            enrollment = TrainingEnrollment.objects.create(**enrollee_data)
            self.stdout.write(f'Created training enrollment: {enrollment.full_name} for {program.title}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created career data:\n'
                f'• {len(job_openings)} Job Openings\n'
                f'• {len(training_programs)} Training Programs\n'
                f'• {len(sample_applicants)} Job Applications\n'
                f'• {len(sample_enrollees)} Training Enrollments'
            )
        )