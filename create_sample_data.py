import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_config.settings')
django.setup()

from django.contrib.auth.models import User
from lms_core.models import Category, Course, Lesson

def run():
    print("Populating sample data...")

    # Create Superuser/Instructor
    instructor, created = User.objects.get_or_create(
        username="instructor",
        email="instructor@example.com",
    )
    if created:
        instructor.set_password("instructor123")
        instructor.is_superuser = True
        instructor.is_staff = True
        instructor.save()
        print("Created superuser 'instructor' with password 'instructor123'")
    else:
        print("Instructor already exists")

    # Create Categories
    cs_cat, _ = Category.objects.get_or_create(name="Computer Science")
    design_cat, _ = Category.objects.get_or_create(name="Design")
    marketing_cat, _ = Category.objects.get_or_create(name="Marketing")

    # Create Course 1: Python
    python_course, p_created = Course.objects.get_or_create(
        code="CS101",
        defaults={
            'instructor': instructor,
            'category': cs_cat,
            'title': "Intro to Python Programming",
            'description': "Learn the fundamentals of Python, the most popular programming language in the world. Ideal for beginners, this course covers syntax, basic data structures, loops, and custom functions, positioning you for data science or web development.",
            'duration': 10,
            'level': "Beginner",
            'is_published': True
        }
    )
    if p_created:
        print("Created Course: Intro to Python Programming")

    # Create Lessons for Course 1
    Lesson.objects.get_or_create(
        course=python_course,
        order=1,
        defaults={
            'title': "Getting Started with Python",
            'description': "Install Python, set up your local development environment, and write your very first script.",
            'content': "Welcome to Intro to Python Programming!\n\nTo get started, you'll need Python installed on your local machine. Download the latest version from python.org.\n\nOnce installed, you can verify it in your terminal by running:\npython --version\n\nNext, write your first script. Create a file named hello.py and add the following code:\nprint('Hello, world!')\n\nRun the file using:\npython hello.py\n\nCongratulations! You have successfully configured your workspace.",
            'is_preview': True
        }
    )

    Lesson.objects.get_or_create(
        course=python_course,
        order=2,
        defaults={
            'title': "Variables and Basic Types",
            'description': "Learn how variables work in Python and explore core data types: integers, floats, strings, and booleans.",
            'content': "In Python, variables are dynamically typed. This means you don't need to declare their type explicitly when creating them.\n\nHere are some examples:\nx = 5  # Integer\ny = 3.14  # Float\nname = 'EduPlatform'  # String\nis_active = True  # Boolean\n\nYou can perform math operations on numeric types, concatenate strings, and use booleans for logical checking. Practice declaring variables in your interactive interpreter.",
            'is_preview': False
        }
    )

    Lesson.objects.get_or_create(
        course=python_course,
        order=3,
        defaults={
            'title': "Control Flow and Conditionals",
            'description': "Understand how to direct the flow of your program using if, elif, and else statements.",
            'content': "Conditional statements allow your program to make decisions based on values and logic.\n\nExample:\nage = 18\nif age >= 18:\n    print('You are authorized to enroll.')\nelse:\n    print('Parental consent is required.')\n\nMake sure to note Python's indentation structure! It uses indentation rather than brackets to mark blocks of code.",
            'is_preview': False
        }
    )

    # Create Course 2: UI/UX
    uiux_course, u_created = Course.objects.get_or_create(
        code="DS102",
        defaults={
            'instructor': instructor,
            'category': design_cat,
            'title': "UI/UX Foundations",
            'description': "Master the fundamentals of user experience design. Learn design thinking principles, color theory, spacing, typography, and interactive wireframing to build beautiful products.",
            'duration': 6,
            'level': "Intermediate",
            'is_published': True
        }
    )
    if u_created:
        print("Created Course: UI/UX Foundations")

    # Create Lessons for Course 2
    Lesson.objects.get_or_create(
        course=uiux_course,
        order=1,
        defaults={
            'title': "Introduction to Design Thinking",
            'description': "Learn the 5 phases of Design Thinking: Empathize, Define, Ideate, Prototype, and Test.",
            'content': "Design thinking is a human-centered approach to innovation that integrates the needs of people, the possibilities of technology, and the requirements for business success.\n\nPhases:\n1. Empathize: Understand user needs.\n2. Define: State your user's problems.\n3. Ideate: Challenge assumptions and create ideas.\n4. Prototype: Start creating solutions.\n5. Test: Try your prototypes out.",
            'is_preview': True
        }
    )

    Lesson.objects.get_or_create(
        course=uiux_course,
        order=2,
        defaults={
            'title': "Wireframing & Prototyping Basics",
            'description': "Transition from low-fidelity paper sketches to high-fidelity interactive digital wireframes.",
            'content': "Wireframes are simple block layouts representing screen structures and content hierarchy. They focus on what a screen does, not what it looks like.\n\nUse tools like Figma to build low-fidelity shapes, then link pages together to create interactive mockups that users can test.",
            'is_preview': False
        }
    )

    print("Data population completed successfully!")

if __name__ == '__main__':
    run()
