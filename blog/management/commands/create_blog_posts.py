from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blog.models import BlogPost


class Command(BaseCommand):
    help = 'Create sample blog posts with YouTube videos for testing'

    def handle(self, *args, **options):
        # Clear existing blog posts
        BlogPost.objects.all().delete()
        
        # Sample blog posts data
        posts_data = [
            {
                'title': 'Top 5 Physiotherapy Exercises for Back Pain Relief',
                'headline': 'Learn effective exercises to relieve chronic back pain and improve your posture at home.',
                'youtube_url': 'https://www.youtube.com/watch?v=4BOTvaRaDjI',
                'description': '''This comprehensive video demonstrates 5 proven physiotherapy exercises that can help alleviate back pain and strengthen your core muscles. These exercises are safe for most people and can be done at home with no special equipment.

Dr. Pratap Bag explains the proper technique for each exercise and provides modifications for different fitness levels. Regular practice of these exercises can significantly reduce back pain and improve your overall spinal health.''',
                'key_points': '''Proper warm-up techniques before exercising
Cat-cow stretches for spinal flexibility
Pelvic tilts for core strengthening
Bridge exercises for lower back support
Child's pose for relaxation and stretching
Cool-down and breathing techniques''',
                'category': 'physiotherapy',
                'tags': 'back pain, physiotherapy, exercises, stretching, core strength, posture',
                'status': 'published',
                'is_featured': True,
            },
            {
                'title': 'Acupressure Points for Instant Headache Relief',
                'headline': 'Discover powerful acupressure techniques to naturally relieve headaches and migraines without medication.',
                'youtube_url': 'https://www.youtube.com/watch?v=LT_dFRnmdGs',
                'description': '''Learn about the most effective acupressure points for treating headaches and migraines. Dr. Pratap Bag demonstrates the exact location of pressure points and the proper technique for applying pressure.

This ancient healing technique can provide immediate relief from tension headaches, stress-related headaches, and even migraines. The video includes detailed instructions on how to locate each pressure point and the duration of pressure application.''',
                'key_points': '''Locating the temple pressure points
Applying pressure to the base of the skull
Using thumb pressure on hand acupoints
Forehead and eyebrow pressure techniques
Neck and shoulder pressure point massage
Breathing techniques during acupressure''',
                'category': 'acupressure',
                'tags': 'headache relief, acupressure, pressure points, migraine, natural healing',
                'status': 'published',
                'is_featured': True,
            },
            {
                'title': 'Therapeutic Massage Techniques for Stress Relief',
                'headline': 'Professional massage techniques you can use at home to reduce stress and muscle tension.',
                'youtube_url': 'https://www.youtube.com/watch?v=_4KQCY69j-o',
                'description': '''Discover professional massage techniques that can help reduce stress, improve circulation, and relieve muscle tension. This video covers basic massage strokes that are safe and effective for self-massage or partner massage.

Dr. Pratap Bag explains the benefits of therapeutic massage and demonstrates proper hand positions, pressure application, and stroke techniques. Learn how to create a relaxing massage routine that fits into your daily wellness practice.''',
                'key_points': '''Basic massage stroke techniques
Proper hand positioning and pressure
Self-massage techniques for neck and shoulders
Partner massage for back and legs
Creating a relaxing environment
Benefits of regular massage therapy''',
                'category': 'massage',
                'tags': 'massage therapy, stress relief, relaxation, self-massage, wellness',
                'status': 'published',
                'is_featured': False,
            },
            {
                'title': 'Daily Stretching Routine for Office Workers',
                'headline': 'Simple stretches to combat the effects of prolonged sitting and improve workplace wellness.',
                'youtube_url': 'https://www.youtube.com/watch?v=RqcOCBb4arc',
                'description': '''Office workers often experience neck pain, back stiffness, and poor posture due to prolonged sitting. This video provides a comprehensive stretching routine specifically designed for people who work at desks.

The routine includes stretches that can be done at your desk during work breaks, as well as a more complete routine for home practice. Each stretch is demonstrated clearly with proper form and safety tips.''',
                'key_points': '''Desk-friendly stretches for work breaks
Neck and shoulder tension relief
Hip flexor stretches for seated workers
Spinal twists for back mobility
Eye exercises for computer users
Creating healthy workplace habits''',
                'category': 'exercise',
                'tags': 'office stretches, desk exercises, workplace wellness, posture, sitting',
                'status': 'published',
                'is_featured': False,
            },
            {
                'title': 'Natural Pain Management Techniques',
                'headline': 'Explore drug-free methods for managing chronic pain using alternative medicine approaches.',
                'youtube_url': 'https://www.youtube.com/watch?v=FIxYCDbRGJc',
                'description': '''This educational video explores various natural pain management techniques that can be used alongside or as alternatives to conventional pain medication. Dr. Pratap Bag shares evidence-based approaches from alternative medicine.

Learn about breathing techniques, mindfulness practices, and physical therapies that can help manage chronic pain conditions. The video also covers when to seek professional help and how to integrate these techniques into a comprehensive pain management plan.''',
                'key_points': '''Understanding chronic pain mechanisms
Breathing techniques for pain relief
Mindfulness and meditation practices
Heat and cold therapy applications
Gentle movement for pain management
Creating a personal pain management plan''',
                'category': 'pain_management',
                'tags': 'pain management, natural healing, chronic pain, alternative medicine, mindfulness',
                'status': 'published',
                'is_featured': False,
            },
            {
                'title': 'Nutrition for Joint Health and Inflammation',
                'headline': 'Discover foods that can help reduce inflammation and support healthy joints naturally.',
                'youtube_url': 'https://www.youtube.com/watch?v=aUaInS6HIGo',
                'description': '''Learn about the powerful connection between nutrition and joint health. This video explores anti-inflammatory foods and dietary strategies that can help reduce joint pain and support overall joint function.

Dr. Pratap Bag discusses which foods to include and avoid for optimal joint health, along with simple meal planning tips. The video also covers supplements that may benefit joint health when used appropriately.''',
                'key_points': '''Anti-inflammatory foods for joint health
Foods to avoid that increase inflammation
Omega-3 fatty acids and joint function
Antioxidant-rich foods for healing
Hydration and joint lubrication
Simple meal planning for joint health''',
                'category': 'nutrition',
                'tags': 'nutrition, joint health, anti-inflammatory, diet, wellness, healthy eating',
                'status': 'published',
                'is_featured': False,
            },
            {
                'title': 'Mental Wellness and Physical Health Connection',
                'headline': 'Understanding how mental health impacts physical well-being and vice versa.',
                'youtube_url': 'https://www.youtube.com/watch?v=ZFCn5rP3VHM',
                'description': '''Explore the important connection between mental wellness and physical health. This video discusses how stress, anxiety, and mental health conditions can manifest as physical symptoms and affect overall health.

Learn practical strategies for improving both mental and physical well-being through integrated approaches including movement, mindfulness, and lifestyle modifications that support both mind and body.''',
                'key_points': '''Mind-body connection in health
How stress affects physical symptoms
Relaxation techniques for mental wellness
Physical activities that boost mood
Creating healthy daily routines
Building resilience and coping skills''',
                'category': 'mental_health',
                'tags': 'mental health, mind-body connection, stress management, wellness, holistic health',
                'status': 'published',
                'is_featured': False,
            },
            {
                'title': 'Post-Injury Rehabilitation Basics',
                'headline': 'Essential rehabilitation principles for safe recovery from common injuries.',
                'youtube_url': 'https://www.youtube.com/watch?v=QivhXlM4NJI',
                'description': '''This educational video covers the fundamental principles of post-injury rehabilitation. Whether recovering from a sports injury, workplace injury, or accident, understanding proper rehabilitation is crucial for complete recovery.

Dr. Pratap Bag explains the phases of healing, appropriate exercises for different recovery stages, and when to progress or modify activities. Safety guidelines and red flags that require immediate medical attention are also covered.''',
                'key_points': '''Understanding the healing process
Early stage rehabilitation principles
Progressive exercise protocols
Pain vs. normal discomfort during recovery
When to seek professional help
Preventing re-injury through proper rehabilitation''',
                'category': 'rehabilitation',
                'tags': 'injury recovery, rehabilitation, healing, physiotherapy, exercise therapy',
                'status': 'published',
                'is_featured': False,
            }
        ]
        
        # Create blog posts
        for post_data in posts_data:
            # Generate slug from title
            post_data['slug'] = slugify(post_data['title'])
            
            # Create the blog post
            blog_post = BlogPost.objects.create(**post_data)
            
            self.stdout.write(
                self.style.SUCCESS(f'Created blog post: {blog_post.title}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(posts_data)} blog posts!')
        )