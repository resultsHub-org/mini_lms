from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Category, Course, Lesson, Enrollment, Progress, Announcement

# Course Views
@login_required
def course_list(request):
    """
    Displays a list of all available courses, filtering based on enrollment states.
    """
    courses = Course.objects.all()
    enrolled_courses = Enrollment.objects.filter(user=request.user).values_list('course_id', flat=True)
    return render(request, 'lms_core/course_list.html', {
        'courses': courses,
        'enrolled_courses': enrolled_courses
    })

def course_detail(request, course_id):
    """
    Displays details for a single course, showing progress statistics if enrolled.
    """
    course = get_object_or_404(Course, pk=course_id)
    
    enrolled = False
    completed_lessons_ids = []
    progress_percent = 0
    completed_count = 0
    total_lessons = course.lessons.count()

    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
        if enrolled:
            completed_lessons_ids = Progress.objects.filter(
                user=request.user, 
                lesson__course=course, 
                completed=True
            ).values_list('lesson_id', flat=True)
            completed_count = len(completed_lessons_ids)
            progress_percent = int(completed_count / total_lessons * 100) if total_lessons > 0 else 0

    return render(request, 'lms_core/course_detail.html', {
        'course': course,
        'enrolled': enrolled,
        'completed_lessons_ids': completed_lessons_ids,
        'progress_percent': progress_percent,
        'completed_count': completed_count,
        'total_lessons': total_lessons
    })

# Lesson Views
@login_required
def lesson_detail(request, course_id, lesson_id):
    """
    Displays the content of a single lesson with active workspace navigation.
    Users must be enrolled to view a lesson.
    """
    course = get_object_or_404(Course, pk=course_id)
    lesson = get_object_or_404(Lesson, pk=lesson_id, course=course)

    # Check if the user is enrolled in the course
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        return redirect('lms_core:course_detail', course_id=course.id)

    # Sidebar data
    lessons = course.lessons.all()
    completed_lessons_ids = set(
        Progress.objects.filter(user=request.user, lesson__course=course, completed=True)
        .values_list('lesson_id', flat=True)
    )

    # Next lesson tracking
    next_lesson = course.lessons.filter(order__gt=lesson.order).first()
    
    # Progress check on the current lesson
    is_completed = Progress.objects.filter(user=request.user, lesson=lesson, completed=True).exists()

    return render(request, 'lms_core/lesson_viewer.html', {
        'course': course,
        'lesson': lesson,
        'lessons': lessons,
        'completed_lessons_ids': completed_lessons_ids,
        'next_lesson': next_lesson,
        'is_completed': is_completed
    })

# Enrollment and Progress Views
@login_required
def enroll_in_course(request, course_id):
    """
    Enrolls the current user in a course.
    """
    course = get_object_or_404(Course, pk=course_id)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    return redirect('lms_core:course_detail', course_id=course.id)

@login_required
def mark_lesson_complete(request, lesson_id):
    """
    Marks a lesson as complete and redirects smart-forward to next index.
    """
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    progress, created = Progress.objects.get_or_create(user=request.user, lesson=lesson)
    progress.completed = True
    progress.completed_at = timezone.now()
    progress.save()

    # Track overall course completion
    total_lessons = lesson.course.lessons.count()
    completed_lessons = Progress.objects.filter(user=request.user, lesson__course=lesson.course, completed=True).count()
    if total_lessons == completed_lessons:
        enrollment = Enrollment.objects.filter(user=request.user, course=lesson.course).first()
        if enrollment and not enrollment.completed:
            enrollment.completed = True
            enrollment.completed_at = timezone.now()
            enrollment.save()

    # Redirect to next lesson
    next_lesson = Lesson.objects.filter(course=lesson.course, order__gt=lesson.order).first()
    if next_lesson:
        return redirect('lms_core:lesson_detail', course_id=lesson.course.id, lesson_id=next_lesson.id)
    
    return redirect('lms_core:course_detail', course_id=lesson.course.id)

